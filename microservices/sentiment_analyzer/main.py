#!/usr/bin/env python3
"""
AGI Sentiment Analyzer Microservice
Advanced sentiment analysis using Vertex AI and custom models
"""

import os
import json
import base64
from datetime import datetime
from typing import Dict, Any, List
import logging
from google.cloud import pubsub_v1
from google.cloud import aiplatform
from google.cloud import language_v1
import functions_framework
from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGISentimentAnalyzer:
    """Advanced sentiment analysis with multiple AI models"""
    
    def __init__(self):
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        self.region = os.environ.get('REGION', 'us-central1')
        
        # Initialize clients
        self.language_client = language_v1.LanguageServiceClient()
        self.publisher = pubsub_v1.PublisherClient()
        
        # Initialize Vertex AI
        aiplatform.init(project=self.project_id, location=self.region)
        
    def analyze_with_natural_language_api(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using Cloud Natural Language API"""
        try:
            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            
            # Get sentiment
            sentiment_response = self.language_client.analyze_sentiment(
                request={"document": document}
            )
            
            # Get entities
            entities_response = self.language_client.analyze_entities(
                request={"document": document}
            )
            
            # Get syntax
            syntax_response = self.language_client.analyze_syntax(
                request={"document": document}
            )
            
            return {
                "sentiment": {
                    "score": sentiment_response.document_sentiment.score,
                    "magnitude": sentiment_response.document_sentiment.magnitude,
                    "classification": self._classify_sentiment(sentiment_response.document_sentiment.score)
                },
                "entities": [
                    {
                        "name": entity.name,
                        "type": entity.type_.name,
                        "salience": entity.salience,
                        "sentiment": {
                            "score": entity.sentiment.score if hasattr(entity, 'sentiment') else 0,
                            "magnitude": entity.sentiment.magnitude if hasattr(entity, 'sentiment') else 0
                        }
                    }
                    for entity in entities_response.entities
                ],
                "key_phrases": [
                    token.text.content 
                    for token in syntax_response.tokens 
                    if token.part_of_speech.tag.name in ['NOUN', 'ADJ']
                ][:10]
            }
            
        except Exception as e:
            logger.error(f"Error in Natural Language API analysis: {e}")
            return {"error": str(e)}
    
    def _classify_sentiment(self, score: float) -> str:
        """Classify sentiment score into categories"""
        if score >= 0.25:
            return "positive"
        elif score <= -0.25:
            return "negative"
        else:
            return "neutral"
    
    def analyze_financial_sentiment(self, text: str, entities: List[Dict]) -> Dict[str, Any]:
        """Advanced financial sentiment analysis"""
        financial_keywords = {
            "bullish": ["growth", "increase", "profit", "bullish", "buy", "strong", "outperform"],
            "bearish": ["decline", "loss", "bearish", "sell", "weak", "underperform", "risk"],
            "neutral": ["stable", "maintain", "hold", "neutral", "unchanged"]
        }
        
        text_lower = text.lower()
        sentiment_signals = {"bullish": 0, "bearish": 0, "neutral": 0}
        
        # Count financial sentiment keywords
        for sentiment, keywords in financial_keywords.items():
            for keyword in keywords:
                sentiment_signals[sentiment] += text_lower.count(keyword)
        
        # Analyze entity sentiment
        financial_entities = []
        for entity in entities:
            if entity["type"] in ["ORGANIZATION", "PERSON"] and entity["salience"] > 0.1:
                financial_entities.append({
                    "name": entity["name"],
                    "sentiment": entity["sentiment"]["score"],
                    "importance": entity["salience"]
                })
        
        # Calculate overall financial sentiment
        total_signals = sum(sentiment_signals.values())
        financial_sentiment = "neutral"
        
        if total_signals > 0:
            bullish_ratio = sentiment_signals["bullish"] / total_signals
            bearish_ratio = sentiment_signals["bearish"] / total_signals
            
            if bullish_ratio > 0.4:
                financial_sentiment = "bullish"
            elif bearish_ratio > 0.4:
                financial_sentiment = "bearish"
        
        return {
            "financial_sentiment": financial_sentiment,
            "sentiment_signals": sentiment_signals,
            "financial_entities": financial_entities,
            "confidence": max(sentiment_signals.values()) / max(total_signals, 1)
        }
    
    def process_news_article(self, article_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single news article for sentiment analysis"""
        try:
            # Extract text content
            title = article_data.get("title", "")
            description = article_data.get("description", "")
            full_text = f"{title}. {description}"
            
            logger.info(f"Analyzing sentiment for article: {title[:50]}...")
            
            # Perform sentiment analysis
            analysis_result = self.analyze_with_natural_language_api(full_text)
            
            if "error" not in analysis_result:
                # Add financial sentiment analysis
                financial_analysis = self.analyze_financial_sentiment(
                    full_text, 
                    analysis_result["entities"]
                )
                
                # Combine results
                complete_analysis = {
                    "article_info": {
                        "source": article_data.get("source"),
                        "title": title,
                        "link": article_data.get("link"),
                        "published": article_data.get("published"),
                        "priority": article_data.get("priority")
                    },
                    "sentiment_analysis": analysis_result["sentiment"],
                    "entities": analysis_result["entities"],
                    "key_phrases": analysis_result["key_phrases"],
                    "financial_analysis": financial_analysis,
                    "processing_timestamp": datetime.now().isoformat(),
                    "analyzer_version": "1.0.0"
                }
                
                return complete_analysis
            else:
                return {"error": analysis_result["error"], "article": article_data}
                
        except Exception as e:
            logger.error(f"Error processing article: {e}")
            return {"error": str(e), "article": article_data}
    
    def publish_analysis_result(self, analysis_result: Dict[str, Any]):
        """Publish analysis result to Pub/Sub"""
        try:
            topic_path = self.publisher.topic_path(self.project_id, "sentiment-analysis-results")
            
            message_data = json.dumps(analysis_result).encode('utf-8')
            
            attributes = {
                "source": analysis_result.get("article_info", {}).get("source", "unknown"),
                "sentiment": analysis_result.get("sentiment_analysis", {}).get("classification", "unknown"),
                "financial_sentiment": analysis_result.get("financial_analysis", {}).get("financial_sentiment", "unknown"),
                "timestamp": analysis_result.get("processing_timestamp", "")
            }
            
            future = self.publisher.publish(topic_path, message_data, **attributes)
            message_id = future.result()
            
            logger.info(f"Published sentiment analysis result: {message_id}")
            
        except Exception as e:
            logger.error(f"Error publishing analysis result: {e}")

# Cloud Function handler for Pub/Sub trigger
@functions_framework.cloud_event
def process_news_sentiment(cloud_event):
    """Process news article sentiment via Pub/Sub trigger"""
    analyzer = AGISentimentAnalyzer()
    
    # Decode Pub/Sub message
    pubsub_message = base64.b64decode(cloud_event.data['message']['data']).decode('utf-8')
    article_data = json.loads(pubsub_message)
    
    logger.info(f"Processing sentiment for article from {article_data.get('source', 'unknown')}")
    
    # Analyze sentiment
    analysis_result = analyzer.process_news_article(article_data)
    
    # Publish result
    if "error" not in analysis_result:
        analyzer.publish_analysis_result(analysis_result)
        return {"status": "success", "article_title": article_data.get("title", "")[:50]}
    else:
        logger.error(f"Analysis failed: {analysis_result['error']}")
        return {"status": "error", "error": analysis_result["error"]}

# FastAPI web server for direct API access
app = FastAPI(title="AGI Sentiment Analyzer", version="1.0.0")
analyzer = AGISentimentAnalyzer()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sentiment-analyzer", "timestamp": datetime.now().isoformat()}

@app.post("/analyze")
async def analyze_text(request: Dict[str, Any]):
    """Analyze sentiment of provided text"""
    text = request.get("text", "")
    if not text:
        return {"error": "No text provided"}
    
    # Create mock article data for analysis
    article_data = {
        "title": text[:100],
        "description": text,
        "source": "direct_api",
        "priority": "high"
    }
    
    result = analyzer.process_news_article(article_data)
    return result

@app.post("/analyze-article")
async def analyze_article(article_data: Dict[str, Any]):
    """Analyze sentiment of a news article"""
    result = analyzer.process_news_article(article_data)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))