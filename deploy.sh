#!/bin/bash

echo "🚀 Deploying Frontline Worker AI System..."

# Set your project
PROJECT_ID="frontline-ai-hackathon"
FUNCTION_NAME="frontline-ai"

gcloud config set project $PROJECT_ID

# Enable required services
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable firestore.googleapis.com

# Deploy the function
gcloud functions deploy $FUNCTION_NAME \
    --gen2 \
    --runtime=python311 \
    --region=us-central1 \
    --source=. \
    --entry-point=frontline_ai \
    --trigger-http \
    --allow-unauthenticated \
    --memory=512MB \
    --timeout=300s \
    --set-env-vars=GCP_PROJECT=$PROJECT_ID

echo "✅ Deployment complete!"
echo "🌐 Your Cloud Function URL:"
gcloud functions describe $FUNCTION_NAME --region=us-central1 --format="value(httpsTrigger.url)"
