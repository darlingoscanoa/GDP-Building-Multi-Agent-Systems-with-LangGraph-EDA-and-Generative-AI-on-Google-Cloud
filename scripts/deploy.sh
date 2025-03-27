#!/bin/bash

# AiDemy Deployment Script
# This is an enhanced version of the original Google Codelab project deployment script

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Check required environment variables
required_vars=(
    "GOOGLE_CLOUD_PROJECT"
    "COURSE_BUCKET_NAME"
    "ASSIGNMENT_BUCKET_NAME"
    "DB_HOST"
    "DB_NAME"
    "DB_USER"
    "DB_PASSWORD"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: Required environment variable $var is not set"
        exit 1
    fi
done

# Set default values
REGION="us-central1"
SERVICE_ACCOUNT_NAME=$(gcloud compute project-info describe --format="value(defaultServiceAccount)")

echo "🚀 Starting AiDemy deployment..."

# Enable required APIs
echo "📦 Enabling required APIs..."
gcloud services enable \
    compute.googleapis.com \
    storage.googleapis.com \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    eventarc.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    cloudbuild.googleapis.com \
    cloudresourcemanager.googleapis.com \
    cloudfunctions.googleapis.com

# Set up service account permissions
echo "🔑 Setting up service account permissions..."
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
    --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
    --role="roles/pubsub.publisher"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
    --role="roles/pubsub.subscriber"

gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
    --role="roles/cloudsql.editor"

# Create Artifact Registry repository
echo "🏗️ Creating Artifact Registry repository..."
gcloud artifacts repositories create agent-repository \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for AiDemy agents"

# Build and push Docker images
echo "🐳 Building and pushing Docker images..."
for service in portal planner courses bookprovider assignment; do
    echo "Building $service..."
    docker build -t $REGION-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/agent-repository/$service:latest ./$service
    docker push $REGION-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/agent-repository/$service:latest
done

# Deploy services to Cloud Run
echo "🚀 Deploying services to Cloud Run..."
for service in portal planner courses bookprovider assignment; do
    echo "Deploying $service..."
    gcloud run deploy aidemy-$service \
        --image $REGION-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/agent-repository/$service:latest \
        --platform managed \
        --region $REGION \
        --allow-unauthenticated \
        --set-env-vars=GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
        --set-env-vars=COURSE_BUCKET_NAME=$COURSE_BUCKET_NAME \
        --set-env-vars=ASSIGNMENT_BUCKET_NAME=$ASSIGNMENT_BUCKET_NAME
done

# Set up Eventarc triggers
echo "⚡ Setting up Eventarc triggers..."
gcloud eventarc triggers create portal-assignment-trigger \
    --location=$REGION \
    --service-account=$SERVICE_ACCOUNT_NAME \
    --destination-run-service=aidemy-portal \
    --destination-run-region=$REGION \
    --destination-run-path="/render_assignment" \
    --event-filters="bucket=$ASSIGNMENT_BUCKET_NAME" \
    --event-filters="type=google.cloud.storage.object.v1.finalized"

# Create Cloud SQL instance
echo "🗄️ Creating Cloud SQL instance..."
gcloud sql instances create aidemy \
    --database-version=POSTGRES_13 \
    --cpu=1 \
    --memory=3840MB \
    --region=$REGION

# Set up database
echo "📊 Setting up database..."
gcloud sql databases create aidemy --instance=aidemy
gcloud sql users create aidemy \
    --instance=aidemy \
    --password=$DB_PASSWORD

# Store secrets in Secret Manager
echo "🔐 Storing secrets in Secret Manager..."
echo -n $DB_USER | gcloud secrets create db-user --data-file=-
echo -n $DB_PASSWORD | gcloud secrets create db-pass --data-file=-
echo -n $DB_NAME | gcloud secrets create db-name --data-file=-

# Create storage buckets
echo "📦 Creating storage buckets..."
gsutil mb -l $REGION gs://$COURSE_BUCKET_NAME
gsutil mb -l $REGION gs://$ASSIGNMENT_BUCKET_NAME

# Set up monitoring
echo "📊 Setting up monitoring..."
gcloud monitoring dashboards create \
    --project=$GOOGLE_CLOUD_PROJECT \
    --display-name="AiDemy Dashboard" \
    --dashboard-file=config/dashboard.json

echo "✅ Deployment completed successfully!"
echo "📝 Service URLs:"
gcloud run services list --platform=managed --region=$REGION --format='value(URL)' 