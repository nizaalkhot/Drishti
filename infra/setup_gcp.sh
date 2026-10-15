#!/usr/bin/env bash
# ==============================================================================
# Drishti — Google Cloud Enterprise Production Provisioning Script
# ==============================================================================
# Sets up Cloud Run, Cloud SQL (PostgreSQL), Memorystore (Redis), VPC Connector,
# Pub/Sub topics, Artifact Registry, and Secret Manager.
# ==============================================================================

set -euo pipefail

# 1. Configuration & Default Variables
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || echo '')}"
REGION="${REGION:-asia-south1}"
VPC_CONNECTOR_NAME="${VPC_CONNECTOR_NAME:-drishti-vpc-conn}"
DB_INSTANCE_NAME="${DB_INSTANCE_NAME:-drishti-pg-16}"
DB_NAME="${DB_NAME:-drishti_db}"
DB_USER="${DB_USER:-drishti_app}"
DB_PASS="${DB_PASS:-$(openssl rand -base64 16)}"
REDIS_INSTANCE_NAME="${REDIS_INSTANCE_NAME:-drishti-redis}"
SERVICE_ACCOUNT_NAME="drishti-cloudrun-sa"

if [ -z "$PROJECT_ID" ]; then
  echo "ERROR: PROJECT_ID is not set. Run 'gcloud config set project <YOUR_PROJECT_ID>' or export PROJECT_ID."
  exit 1
fi

echo "=================================================================="
echo "Starting Drishti Production Infrastructure Provisioning"
echo "Project ID : $PROJECT_ID"
echo "Region     : $REGION"
echo "=================================================================="

# 2. Enable Required GCP APIs
echo "--> [1/8] Enabling Google Cloud Services & APIs..."
gcloud services enable \
  run.googleapis.com \
  sqladmin.googleapis.com \
  redis.googleapis.com \
  pubsub.googleapis.com \
  secretmanager.googleapis.com \
  vpcaccess.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  bigquery.googleapis.com \
  aiplatform.googleapis.com \
  --project="$PROJECT_ID"

# 3. Create Artifact Registry Docker Repository
echo "--> [2/8] Setting up Artifact Registry..."
if ! gcloud artifacts repositories describe drishti --location="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud artifacts repositories create drishti \
    --repository-format=docker \
    --location="$REGION" \
    --description="Drishti Docker Container Repository" \
    --project="$PROJECT_ID"
  echo "    Artifact repository 'drishti' created."
else
  echo "    Artifact repository 'drishti' already exists."
fi

# 4. Create Serverless VPC Access Connector
echo "--> [3/8] Setting up Serverless VPC Access Connector ($VPC_CONNECTOR_NAME)..."
if ! gcloud compute networks vpc-access connectors describe "$VPC_CONNECTOR_NAME" --region="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud compute networks vpc-access connectors create "$VPC_CONNECTOR_NAME" \
    --region="$REGION" \
    --network=default \
    --range=10.8.0.0/28 \
    --min-instances=2 \
    --max-instances=10 \
    --machine-type=e2-micro \
    --project="$PROJECT_ID"
  echo "    VPC Connector '$VPC_CONNECTOR_NAME' created."
else
  echo "    VPC Connector '$VPC_CONNECTOR_NAME' already exists."
fi

# 5. Create Cloud SQL (PostgreSQL 16) Instance
echo "--> [4/8] Provisioning Cloud SQL PostgreSQL 16 ($DB_INSTANCE_NAME)..."
if ! gcloud sql instances describe "$DB_INSTANCE_NAME" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud sql instances create "$DB_INSTANCE_NAME" \
    --database-version=POSTGRES_16 \
    --tier=db-custom-2-7680 \
    --region="$REGION" \
    --storage-size=20GB \
    --storage-auto-increase \
    --availability-type=REGIONAL \
    --backup \
    --retained-backups-count=7 \
    --project="$PROJECT_ID"
  echo "    Cloud SQL instance created."

  # Create Database & User
  gcloud sql databases create "$DB_NAME" --instance="$DB_INSTANCE_NAME" --project="$PROJECT_ID"
  gcloud sql users create "$DB_USER" --instance="$DB_INSTANCE_NAME" --password="$DB_PASS" --project="$PROJECT_ID"
else
  echo "    Cloud SQL instance '$DB_INSTANCE_NAME' already exists."
fi

# 6. Create Cloud Memorystore (Redis) Instance
echo "--> [5/8] Provisioning Cloud Memorystore Redis ($REDIS_INSTANCE_NAME)..."
if ! gcloud redis instances describe "$REDIS_INSTANCE_NAME" --region="$REGION" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud redis instances create "$REDIS_INSTANCE_NAME" \
    --size=1 \
    --region="$REGION" \
    --network=default \
    --tier=BASIC \
    --redis-version=redis_7_0 \
    --project="$PROJECT_ID"
  echo "    Memorystore Redis instance created."
else
  echo "    Memorystore Redis instance '$REDIS_INSTANCE_NAME' already exists."
fi

# Fetch Redis Host IP
REDIS_HOST=$(gcloud redis instances describe "$REDIS_INSTANCE_NAME" --region="$REGION" --project="$PROJECT_ID" --format="value(host)" || echo "")
REDIS_PORT=$(gcloud redis instances describe "$REDIS_INSTANCE_NAME" --region="$REGION" --project="$PROJECT_ID" --format="value(port)" || echo "6379")

# 7. Create Pub/Sub Event Topics
echo "--> [6/8] Provisioning Pub/Sub Event Topics..."
for topic in drishti-transaction-events drishti-fraud-alerts drishti-str-filings; do
  if ! gcloud pubsub topics describe "$topic" --project="$PROJECT_ID" >/dev/null 2>&1; then
    gcloud pubsub topics create "$topic" --project="$PROJECT_ID"
    echo "    Created topic: $topic"
  else
    echo "    Topic $topic already exists."
  fi
done

# 8. Setup IAM Service Account & Secret Manager
echo "--> [7/8] Configuring Service Account and Secret Manager..."
SA_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
if ! gcloud iam service-accounts describe "$SA_EMAIL" --project="$PROJECT_ID" >/dev/null 2>&1; then
  gcloud iam service-accounts create "$SERVICE_ACCOUNT_NAME" \
    --display-name="Drishti Cloud Run Service Account" \
    --project="$PROJECT_ID"
fi

# Grant Cloud Run SA permissions
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/cloudsql.client" >/dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/pubsub.publisher" >/dev/null

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor" >/dev/null

# Construct Connection Strings
DB_SOCKET_URL="postgresql+asyncpg://${DB_USER}:${DB_PASS}@/${DB_NAME}?host=/cloudsql/${PROJECT_ID}:${REGION}:${DB_INSTANCE_NAME}"
REDIS_URL="redis://${REDIS_HOST}:${REDIS_PORT}/0"

# Store Secrets
store_secret() {
  local name="$1"
  local val="$2"
  if ! gcloud secrets describe "$name" --project="$PROJECT_ID" >/dev/null 2>&1; then
    echo -n "$val" | gcloud secrets create "$name" --data-file=- --project="$PROJECT_ID"
  else
    echo -n "$val" | gcloud secrets versions add "$name" --data-file=- --project="$PROJECT_ID"
  fi
}

echo "--> [8/8] Populating Secret Manager secrets..."
store_secret "drishti-db-url" "$DB_SOCKET_URL"
if [ -n "$REDIS_HOST" ]; then
  store_secret "drishti-redis-url" "$REDIS_URL"
fi

echo "=================================================================="
echo "Drishti GCP Production Infrastructure Provisioned Successfully!"
echo "Cloud SQL Instance   : $DB_INSTANCE_NAME"
echo "Memorystore Redis    : $REDIS_HOST:$REDIS_PORT"
echo "VPC Access Connector : $VPC_CONNECTOR_NAME"
echo "Next Step: Run 'gcloud builds submit --config=infra/cloudbuild.yaml' to deploy."
echo "=================================================================="
