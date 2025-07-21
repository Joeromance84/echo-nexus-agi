#!/bin/bash
# AGI Market Analytics Platform Deployment Script

set -e

PROJECT_ID="${GOOGLE_CLOUD_PROJECT}"
REGION="us-central1"

echo "🚀 Starting AGI Market Analytics Platform Deployment"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"

# Enable required APIs
echo "📡 Enabling Google Cloud APIs..."
gcloud services enable     cloudbuild.googleapis.com     cloudfunctions.googleapis.com     run.googleapis.com     pubsub.googleapis.com     bigquery.googleapis.com     aiplatform.googleapis.com     storage.googleapis.com     monitoring.googleapis.com

# Create storage buckets
echo "💾 Creating storage buckets..."
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-market-data-raw
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-market-data-processed
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-ml-models
gsutil mb -p $PROJECT_ID -l $REGION gs://$PROJECT_ID-static-assets

# Create Pub/Sub topics and subscriptions
echo "📨 Creating Pub/Sub topics..."
gcloud pubsub topics create market-data-raw
gcloud pubsub topics create market-data-processed
gcloud pubsub topics create sentiment-analysis
gcloud pubsub topics create prediction-requests
gcloud pubsub topics create prediction-results

gcloud pubsub subscriptions create data-processor-sub --topic=market-data-raw
gcloud pubsub subscriptions create sentiment-analyzer-sub --topic=market-data-processed
gcloud pubsub subscriptions create prediction-engine-sub --topic=sentiment-analysis
gcloud pubsub subscriptions create dashboard-updates-sub --topic=prediction-results

# Create BigQuery dataset
echo "📊 Creating BigQuery datasets..."
bq mk --location=$REGION market_analytics
bq mk --location=$REGION model_training
bq mk --location=$REGION system_metrics

# Deploy Cloud Functions
echo "⚡ Deploying Cloud Functions..."
gcloud functions deploy agi-data-ingestion     --runtime python39     --trigger-bucket $PROJECT_ID-market-data-raw     --memory 1GB     --timeout 540s     --region $REGION

gcloud functions deploy agi-sentiment-analysis     --runtime python39     --trigger-topic market-data-processed     --memory 2GB     --timeout 300s     --region $REGION

gcloud functions deploy agi-prediction-engine     --runtime python39     --trigger-http     --memory 4GB     --timeout 600s     --region $REGION

# Build and deploy Cloud Run services
echo "🏃 Building and deploying Cloud Run services..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/agi-api:latest ./backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/agi-dashboard:latest ./frontend

gcloud run deploy agi-api-server     --image gcr.io/$PROJECT_ID/agi-api:latest     --platform managed     --region $REGION     --cpu 2     --memory 4Gi     --concurrency 100     --max-instances 50     --allow-unauthenticated

gcloud run deploy agi-dashboard     --image gcr.io/$PROJECT_ID/agi-dashboard:latest     --platform managed     --region $REGION     --cpu 1     --memory 2Gi     --concurrency 200     --max-instances 20     --allow-unauthenticated

# Set up Cloud Build triggers
echo "🔧 Creating Cloud Build triggers..."
gcloud builds triggers create github     --repo-name=agi-market-analytics-platform     --repo-owner=$GITHUB_USER     --branch-pattern=^main$     --build-config=cloudbuild-production.yaml

gcloud builds triggers create github     --repo-name=agi-market-analytics-platform     --repo-owner=$GITHUB_USER     --branch-pattern=^feature/.*     --build-config=cloudbuild-staging.yaml

# Deploy monitoring and alerting
echo "📊 Setting up monitoring..."
gcloud alpha monitoring dashboards create --config-from-file=monitoring/dashboards.yaml
gcloud alpha monitoring policies create --policy-from-file=monitoring/alert-policies.yaml

echo "✅ AGI Market Analytics Platform deployed successfully!"
echo "🌐 API Endpoint: $(gcloud run services describe agi-api-server --region=$REGION --format='value(status.url)')"
echo "📊 Dashboard: $(gcloud run services describe agi-dashboard --region=$REGION --format='value(status.url)')"
