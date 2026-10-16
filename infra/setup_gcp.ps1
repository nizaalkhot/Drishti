# ==============================================================================
# Drishti — Google Cloud Enterprise Production Provisioning Script (PowerShell)
# ==============================================================================
# Sets up Cloud Run, Cloud SQL (PostgreSQL), Memorystore (Redis), VPC Connector,
# Pub/Sub topics, Artifact Registry, and Secret Manager.
# ==============================================================================

$ProgressPreference = "SilentlyContinue"
$ErrorActionPreference = "Continue"

$PROJECT_ID = if ($env:PROJECT_ID) { $env:PROJECT_ID } else { "team-gain" }
$REGION = if ($env:REGION) { $env:REGION } else { "asia-south1" }
$VPC_CONNECTOR_NAME = "drishti-vpc-conn"
$DB_INSTANCE_NAME = "drishti-pg-16"
$DB_NAME = "drishti_db"
$DB_USER = "drishti_app"
$DB_PASS = [System.Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes([System.Guid]::NewGuid().ToString()))
$REDIS_INSTANCE_NAME = "drishti-redis"
$SERVICE_ACCOUNT_NAME = "drishti-cloudrun-sa"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Starting Drishti Production Infrastructure Provisioning" -ForegroundColor Green
Write-Host "Project ID : $PROJECT_ID"
Write-Host "Region     : $REGION"
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Enable Required GCP APIs
Write-Host "--> [1/8] Enabling Google Cloud Services & APIs..." -ForegroundColor Yellow
cmd.exe /c "gcloud services enable run.googleapis.com sqladmin.googleapis.com redis.googleapis.com pubsub.googleapis.com secretmanager.googleapis.com vpcaccess.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com bigquery.googleapis.com aiplatform.googleapis.com --project=$PROJECT_ID"

# 2. Check/Create Artifact Registry Docker Repository
Write-Host "--> [2/8] Setting up Artifact Registry..." -ForegroundColor Yellow
cmd.exe /c "gcloud artifacts repositories describe drishti --location=$REGION --project=$PROJECT_ID >nul 2>&1"
if ($LASTEXITCODE -ne 0) {
  cmd.exe /c "gcloud artifacts repositories create drishti --repository-format=docker --location=$REGION --description=""Drishti Docker Repository"" --project=$PROJECT_ID"
  Write-Host "    Artifact repository 'drishti' created." -ForegroundColor Green
} else {
  Write-Host "    Artifact repository 'drishti' already exists." -ForegroundColor Gray
}

# 3. Check/Create Serverless VPC Access Connector
Write-Host "--> [3/8] Setting up Serverless VPC Access Connector ($VPC_CONNECTOR_NAME)..." -ForegroundColor Yellow
cmd.exe /c "gcloud compute networks vpc-access connectors describe $VPC_CONNECTOR_NAME --region=$REGION --project=$PROJECT_ID >nul 2>&1"
if ($LASTEXITCODE -ne 0) {
  cmd.exe /c "gcloud compute networks vpc-access connectors create $VPC_CONNECTOR_NAME --region=$REGION --network=default --range=10.8.0.0/28 --min-instances=2 --max-instances=10 --machine-type=e2-micro --project=$PROJECT_ID"
  Write-Host "    VPC Connector '$VPC_CONNECTOR_NAME' created." -ForegroundColor Green
} else {
  Write-Host "    VPC Connector '$VPC_CONNECTOR_NAME' already exists." -ForegroundColor Gray
}

# 4. Check/Create Cloud SQL (PostgreSQL 16) Instance
Write-Host "--> [4/8] Provisioning Cloud SQL PostgreSQL 16 ($DB_INSTANCE_NAME)..." -ForegroundColor Yellow
cmd.exe /c "gcloud sql instances describe $DB_INSTANCE_NAME --project=$PROJECT_ID >nul 2>&1"
if ($LASTEXITCODE -ne 0) {
  cmd.exe /c "gcloud sql instances create $DB_INSTANCE_NAME --database-version=POSTGRES_16 --tier=db-custom-2-7680 --region=$REGION --storage-size=20GB --storage-auto-increase --availability-type=REGIONAL --backup --retained-backups-count=7 --project=$PROJECT_ID"
  Write-Host "    Cloud SQL instance created." -ForegroundColor Green

  # Create Database & User
  cmd.exe /c "gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE_NAME --project=$PROJECT_ID"
  cmd.exe /c "gcloud sql users create $DB_USER --instance=$DB_INSTANCE_NAME --password=$DB_PASS --project=$PROJECT_ID"
} else {
  Write-Host "    Cloud SQL instance '$DB_INSTANCE_NAME' already exists." -ForegroundColor Gray
}

# 5. Check/Create Cloud Memorystore (Redis) Instance
Write-Host "--> [5/8] Provisioning Cloud Memorystore Redis ($REDIS_INSTANCE_NAME)..." -ForegroundColor Yellow
cmd.exe /c "gcloud redis instances describe $REDIS_INSTANCE_NAME --region=$REGION --project=$PROJECT_ID >nul 2>&1"
if ($LASTEXITCODE -ne 0) {
  cmd.exe /c "gcloud redis instances create $REDIS_INSTANCE_NAME --size=1 --region=$REGION --network=default --tier=BASIC --redis-version=redis_7_0 --project=$PROJECT_ID"
  Write-Host "    Memorystore Redis instance created." -ForegroundColor Green
} else {
  Write-Host "    Memorystore Redis instance '$REDIS_INSTANCE_NAME' already exists." -ForegroundColor Gray
}

$REDIS_HOST = cmd.exe /c "gcloud redis instances describe $REDIS_INSTANCE_NAME --region=$REGION --project=$PROJECT_ID --format=""value(host)"" 2>nul"
$REDIS_PORT = cmd.exe /c "gcloud redis instances describe $REDIS_INSTANCE_NAME --region=$REGION --project=$PROJECT_ID --format=""value(port)"" 2>nul"
if (-not $REDIS_PORT) { $REDIS_PORT = "6379" }

# 6. Check/Create Pub/Sub Event Topics
Write-Host "--> [6/8] Provisioning Pub/Sub Event Topics..." -ForegroundColor Yellow
$topics = @("drishti-transaction-events", "drishti-fraud-alerts", "drishti-str-filings")
foreach ($t in $topics) {
  cmd.exe /c "gcloud pubsub topics describe $t --project=$PROJECT_ID >nul 2>&1"
  if ($LASTEXITCODE -ne 0) {
    cmd.exe /c "gcloud pubsub topics create $t --project=$PROJECT_ID"
    Write-Host "    Created topic: $t" -ForegroundColor Green
  } else {
    Write-Host "    Topic $t already exists." -ForegroundColor Gray
  }
}

# 7. Setup IAM Service Account & Secret Manager
Write-Host "--> [7/8] Configuring Service Account and Secret Manager..." -ForegroundColor Yellow
$SA_EMAIL = "${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
cmd.exe /c "gcloud iam service-accounts describe $SA_EMAIL --project=$PROJECT_ID >nul 2>&1"
if ($LASTEXITCODE -ne 0) {
  cmd.exe /c "gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME --display-name=""Drishti Cloud Run Service Account"" --project=$PROJECT_ID"
}

cmd.exe /c "gcloud projects add-iam-policy-binding $PROJECT_ID --member=""serviceAccount:${SA_EMAIL}"" --role=""roles/cloudsql.client"" >nul"
cmd.exe /c "gcloud projects add-iam-policy-binding $PROJECT_ID --member=""serviceAccount:${SA_EMAIL}"" --role=""roles/pubsub.publisher"" >nul"
cmd.exe /c "gcloud projects add-iam-policy-binding $PROJECT_ID --member=""serviceAccount:${SA_EMAIL}"" --role=""roles/secretmanager.secretAccessor"" >nul"

# 8. Store Secrets in Secret Manager
Write-Host "--> [8/8] Populating Secret Manager secrets..." -ForegroundColor Yellow
$DB_SOCKET_URL = "postgresql+asyncpg://${DB_USER}:${DB_PASS}@/${DB_NAME}?host=/cloudsql/${PROJECT_ID}:${REGION}:${DB_INSTANCE_NAME}"
$REDIS_URL = "redis://${REDIS_HOST}:${REDIS_PORT}/0"

function Set-GcpSecret($name, $val) {
  cmd.exe /c "gcloud secrets describe $name --project=$PROJECT_ID >nul 2>&1"
  if ($LASTEXITCODE -ne 0) {
    [System.IO.File]::WriteAllText("$env:TEMP\$name.txt", $val)
    cmd.exe /c "gcloud secrets create $name --data-file=""$env:TEMP\$name.txt"" --project=$PROJECT_ID"
    Remove-Item "$env:TEMP\$name.txt" -Force -ErrorAction SilentlyContinue
  } else {
    [System.IO.File]::WriteAllText("$env:TEMP\$name.txt", $val)
    cmd.exe /c "gcloud secrets versions add $name --data-file=""$env:TEMP\$name.txt"" --project=$PROJECT_ID"
    Remove-Item "$env:TEMP\$name.txt" -Force -ErrorAction SilentlyContinue
  }
}

Set-GcpSecret "drishti-db-url" $DB_SOCKET_URL
if ($REDIS_HOST) {
  Set-GcpSecret "drishti-redis-url" $REDIS_URL
}

Write-Host "==================================================================" -ForegroundColor Green
Write-Host "Drishti GCP Production Infrastructure Provisioned Successfully!" -ForegroundColor Green
Write-Host "Cloud SQL Instance   : $DB_INSTANCE_NAME"
Write-Host "Memorystore Redis    : ${REDIS_HOST}:${REDIS_PORT}"
Write-Host "VPC Access Connector : $VPC_CONNECTOR_NAME"
Write-Host "==================================================================" -ForegroundColor Green
