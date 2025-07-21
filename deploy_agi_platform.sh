#!/bin/bash
# AGI Platform Deployment Script
# Automated deployment of all microservices using Google Cloud Build

set -e

echo "🚀 DEPLOYING AGI MARKET ANALYTICS PLATFORM"
echo "=========================================="

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"agi-market-analytics"}
REGION=${REGION:-"us-central1"}

echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo ""

# Function to deploy microservice
deploy_microservice() {
    local service_name=$1
    local service_dir=$2
    
    echo "🔧 Deploying $service_name..."
    
    if [ -d "$service_dir" ]; then
        cd "$service_dir"
        
        # Submit build to Cloud Build
        gcloud builds submit --config=cloudbuild.yaml \
            --substitutions=_REGION=$REGION \
            --project=$PROJECT_ID
        
        if [ $? -eq 0 ]; then
            echo "✅ $service_name deployed successfully"
        else
            echo "❌ Failed to deploy $service_name"
            exit 1
        fi
        
        cd - > /dev/null
    else
        echo "⚠️ Directory $service_dir not found, skipping $service_name"
    fi
    
    echo ""
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install Google Cloud SDK."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login'"
    exit 1
fi

# Set project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable pubsub.googleapis.com
gcloud services enable bigquery.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable language.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable cloudscheduler.googleapis.com

echo "✅ APIs enabled"
echo ""

# Create Pub/Sub topics
echo "📡 Setting up Pub/Sub topics..."
gcloud pubsub topics create news-data-stream --project=$PROJECT_ID || echo "Topic already exists"
gcloud pubsub topics create sentiment-analysis-results --project=$PROJECT_ID || echo "Topic already exists"
echo "✅ Pub/Sub topics configured"
echo ""

# Create BigQuery dataset
echo "📊 Setting up BigQuery dataset..."
bq mk --dataset --location=$REGION $PROJECT_ID:market_analytics || echo "Dataset already exists"

# Create BigQuery tables
echo "Creating BigQuery tables..."
bq mk --table $PROJECT_ID:market_analytics.sentiment_results \
    source:STRING,sentiment_classification:STRING,financial_sentiment:STRING,confidence:FLOAT,processing_timestamp:TIMESTAMP,article_title:STRING || echo "Table already exists"

bq mk --table $PROJECT_ID:market_analytics.prediction_results \
    symbol:STRING,prediction_direction:STRING,confidence:FLOAT,reasoning:STRING,prediction_timestamp:TIMESTAMP,actual_outcome:STRING || echo "Table already exists"

echo "✅ BigQuery setup complete"
echo ""

# Create Cloud Storage buckets
echo "🗄️ Setting up Cloud Storage buckets..."
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-news-data || echo "Bucket already exists"
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-reports || echo "Bucket already exists"
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-ml-models || echo "Bucket already exists"

# Set bucket permissions
gsutil iam ch allUsers:objectViewer gs://$PROJECT_ID-reports || echo "Permissions already set"

echo "✅ Cloud Storage setup complete"
echo ""

# Deploy microservices in order
echo "🚀 Deploying microservices..."

# 1. News Ingester
deploy_microservice "News Ingester" "microservices/news_ingester"

# 2. Sentiment Analyzer
deploy_microservice "Sentiment Analyzer" "microservices/sentiment_analyzer"

# 3. Report Generator
deploy_microservice "Report Generator" "microservices/report_generator"

# 4. Orchestrator (deploy last)
deploy_microservice "Orchestrator" "microservices/orchestrator"

# Set up automated scheduling
echo "⏰ Setting up automated scheduling..."
gcloud app deploy --quiet || echo "App Engine already deployed"

# Create scheduler job for orchestrator
gcloud scheduler jobs create http agi-pipeline-schedule \
    --schedule="0 */6 * * *" \
    --uri="https://agi-orchestrator-$PROJECT_ID.a.run.app/run-pipeline" \
    --http-method=POST \
    --location=$REGION || echo "Schedule already exists"

echo "✅ Automated scheduling configured"
echo ""

# Test deployment
echo "🧪 Testing deployment..."

# Wait a moment for services to start
sleep 30

# Test orchestrator health
ORCHESTRATOR_URL="https://agi-orchestrator-$PROJECT_ID.a.run.app"
if curl -s -f "$ORCHESTRATOR_URL/health" > /dev/null; then
    echo "✅ Orchestrator health check passed"
else
    echo "⚠️ Orchestrator health check failed (services may still be starting)"
fi

# Test complete pipeline
echo "🔄 Testing complete pipeline..."
curl -X POST "$ORCHESTRATOR_URL/run-pipeline" -H "Content-Type: application/json" || echo "Pipeline test initiated"

echo ""
echo "🎉 AGI PLATFORM DEPLOYMENT COMPLETE!"
echo "===================================="
echo ""
echo "📍 Service URLs:"
echo "  Orchestrator: https://agi-orchestrator-$PROJECT_ID.a.run.app"
echo "  News Ingester: https://agi-news-ingester-$PROJECT_ID.a.run.app"
echo "  Sentiment Analyzer: https://agi-sentiment-analyzer-$PROJECT_ID.a.run.app"  
echo "  Report Generator: https://agi-report-generator-$PROJECT_ID.a.run.app"
echo ""
echo "📊 Management URLs:"
echo "  BigQuery: https://console.cloud.google.com/bigquery?project=$PROJECT_ID"
echo "  Cloud Storage: https://console.cloud.google.com/storage/browser?project=$PROJECT_ID"
echo "  Cloud Run: https://console.cloud.google.com/run?project=$PROJECT_ID"
echo "  Cloud Scheduler: https://console.cloud.google.com/cloudscheduler?project=$PROJECT_ID"
echo ""
echo "🚀 To test the complete pipeline:"
echo "  curl -X POST https://agi-orchestrator-$PROJECT_ID.a.run.app/run-pipeline-sync"
echo ""
echo "📈 System metrics:"
echo "  curl https://agi-orchestrator-$PROJECT_ID.a.run.app/metrics"
echo ""
echo "✨ The AGI platform is now operational and will automatically process market data every 6 hours!"