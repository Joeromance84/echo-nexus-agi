#!/usr/bin/env python3
"""
AGI News Ingester Microservice
Autonomous news monitoring and data ingestion
"""

import os
import json
import time
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import aiohttp
import feedparser
from google.cloud import pubsub_v1
from google.cloud import storage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AGINewsIngester:
    """Autonomous news ingestion microservice"""
    
    def __init__(self):
        self.project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        self.pubsub_topic = os.environ.get('PUBSUB_TOPIC', 'news-data-stream')
        self.storage_bucket = os.environ.get('STORAGE_BUCKET', f'{self.project_id}-news-data')
        
        # Initialize clients
        self.publisher = pubsub_v1.PublisherClient()
        self.storage_client = storage.Client()
        
        # News sources configuration
        self.news_sources = [
            {
                "name": "Reuters Finance",
                "url": "https://feeds.reuters.com/reuters/businessNews",
                "type": "rss",
                "priority": "high"
            },
            {
                "name": "Yahoo Finance",
                "url": "https://feeds.finance.yahoo.com/rss/2.0/headline",
                "type": "rss", 
                "priority": "medium"
            },
            {
                "name": "MarketWatch",
                "url": "https://feeds.marketwatch.com/marketwatch/realtimeheadlines/",
                "type": "rss",
                "priority": "medium"
            }
        ]
        
    async def fetch_rss_feed(self, source: Dict[str, str]) -> List[Dict[str, Any]]:
        """Fetch and parse RSS feed"""
        try:
            logger.info(f"Fetching RSS feed from {source['name']}")
            
            # Parse RSS feed
            feed = feedparser.parse(source['url'])
            
            articles = []
            for entry in feed.entries[:20]:  # Limit to 20 most recent
                article = {
                    "source": source['name'],
                    "title": entry.get('title', ''),
                    "description": entry.get('description', ''),
                    "link": entry.get('link', ''),
                    "published": entry.get('published', ''),
                    "timestamp": datetime.now().isoformat(),
                    "priority": source['priority'],
                    "raw_entry": dict(entry)
                }
                articles.append(article)
            
            logger.info(f"Fetched {len(articles)} articles from {source['name']}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed from {source['name']}: {e}")
            return []
    
    async def publish_to_pubsub(self, articles: List[Dict[str, Any]]):
        """Publish articles to Pub/Sub for downstream processing"""
        topic_path = self.publisher.topic_path(self.project_id, self.pubsub_topic)
        
        for article in articles:
            try:
                # Serialize article data
                message_data = json.dumps(article).encode('utf-8')
                
                # Add message attributes
                attributes = {
                    'source': article['source'],
                    'priority': article['priority'],
                    'timestamp': article['timestamp']
                }
                
                # Publish message
                future = self.publisher.publish(topic_path, message_data, **attributes)
                message_id = future.result()
                
                logger.debug(f"Published article to Pub/Sub: {message_id}")
                
            except Exception as e:
                logger.error(f"Error publishing article to Pub/Sub: {e}")
    
    async def store_raw_data(self, articles: List[Dict[str, Any]]):
        """Store raw article data in Cloud Storage for backup"""
        try:
            bucket = self.storage_client.bucket(self.storage_bucket)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"raw_news/{timestamp}_news_batch.json"
            
            # Upload data
            blob = bucket.blob(filename)
            blob.upload_from_string(json.dumps(articles, indent=2))
            
            logger.info(f"Stored {len(articles)} articles in Cloud Storage: {filename}")
            
        except Exception as e:
            logger.error(f"Error storing raw data: {e}")
    
    async def ingest_news_cycle(self):
        """Complete news ingestion cycle"""
        logger.info("Starting news ingestion cycle")
        
        all_articles = []
        
        # Fetch from all sources concurrently
        tasks = [self.fetch_rss_feed(source) for source in self.news_sources]
        results = await asyncio.gather(*tasks)
        
        # Combine all articles
        for articles in results:
            all_articles.extend(articles)
        
        if all_articles:
            logger.info(f"Total articles fetched: {len(all_articles)}")
            
            # Process articles
            await asyncio.gather(
                self.publish_to_pubsub(all_articles),
                self.store_raw_data(all_articles)
            )
            
            # Generate ingestion report
            report = {
                "timestamp": datetime.now().isoformat(),
                "total_articles": len(all_articles),
                "sources_processed": len(self.news_sources),
                "articles_by_source": {
                    source["name"]: len([a for a in all_articles if a["source"] == source["name"]]) 
                    for source in self.news_sources
                }
            }
            
            logger.info(f"Ingestion cycle completed: {report}")
            return report
        else:
            logger.warning("No articles fetched in this cycle")
            return {"error": "No articles fetched"}
    
    async def run_continuous_ingestion(self, interval_seconds: int = 300):
        """Run continuous news ingestion"""
        logger.info(f"Starting continuous news ingestion (interval: {interval_seconds}s)")
        
        while True:
            try:
                await self.ingest_news_cycle()
                logger.info(f"Waiting {interval_seconds} seconds until next cycle")
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in continuous ingestion: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error

# FastAPI web server for health checks and manual triggers
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="AGI News Ingester", version="1.0.0")
ingester = AGINewsIngester()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "news-ingester", "timestamp": datetime.now().isoformat()}

@app.post("/ingest")
async def manual_ingest():
    """Manually trigger news ingestion"""
    result = await ingester.ingest_news_cycle()
    return result

@app.get("/sources")
async def get_sources():
    """Get configured news sources"""
    return {"sources": ingester.news_sources}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        # Run continuous ingestion
        asyncio.run(ingester.run_continuous_ingestion())
    else:
        # Run web server
        uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))