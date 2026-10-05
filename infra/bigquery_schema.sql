-- Drishti BigQuery Schema DDL
-- Project: team-gain
-- Region: asia-south1 (Mumbai)
-- Dataset: drishti_fraud_lake

CREATE SCHEMA IF NOT EXISTS `team-gain.drishti_fraud_lake`
OPTIONS (
  location = 'asia-south1',
  description = 'Drishti Banking Scam & Mule Graph Data Lake'
);

-- 1. Partitioned Transaction Lake
CREATE TABLE IF NOT EXISTS `team-gain.drishti_fraud_lake.transactions` (
  transaction_id STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  sender_id STRING NOT NULL,
  sender_vpa STRING NOT NULL,
  sender_account STRING NOT NULL,
  receiver_id STRING NOT NULL,
  receiver_vpa STRING NOT NULL,
  receiver_ifsc STRING NOT NULL,
  amount NUMERIC NOT NULL,
  remark STRING,
  device_id STRING,
  ip_address STRING,
  is_call_active BOOL,
  call_duration_minutes FLOAT64,
  accessibility_service_enabled BOOL,
  remote_app_active BOOL,
  risk_score FLOAT64,
  decision STRING,
  scam_typology STRING
)
PARTITION BY DATE(timestamp)
CLUSTER BY receiver_id, sender_id, device_id;

-- 2. Mule Ring Graph Nodes & Accounts
CREATE TABLE IF NOT EXISTS `team-gain.drishti_fraud_lake.mule_accounts` (
  account_id STRING NOT NULL,
  vpa STRING NOT NULL,
  ifsc STRING NOT NULL,
  ring_cluster_id STRING,
  role STRING, -- 'aggregator', 'layering', 'cash_out'
  mule_confidence_score FLOAT64,
  first_seen_timestamp TIMESTAMP,
  last_seen_timestamp TIMESTAMP,
  total_inflow_amount NUMERIC,
  total_outflow_amount NUMERIC,
  rapid_passthrough_ratio FLOAT64,
  status STRING -- 'ACTIVE', 'MONITORED', 'FROZEN'
)
CLUSTER BY ring_cluster_id, account_id;

-- 3. Device Fingerprints & Graph Edges
CREATE TABLE IF NOT EXISTS `team-gain.drishti_fraud_lake.device_fingerprints` (
  device_id STRING NOT NULL,
  linked_account_id STRING NOT NULL,
  ip_address STRING,
  first_associated TIMESTAMP,
  last_associated TIMESTAMP
)
CLUSTER BY device_id, linked_account_id;

-- 4. FIU-IND Suspicious Transaction Reports (STRs)
CREATE TABLE IF NOT EXISTS `team-gain.drishti_fraud_lake.suspicious_transaction_reports` (
  str_reference_no STRING NOT NULL,
  case_id STRING NOT NULL,
  transaction_id STRING NOT NULL,
  suspect_account STRING NOT NULL,
  victim_account STRING NOT NULL,
  transaction_amount NUMERIC NOT NULL,
  grounds_of_suspicion STRING,
  verified_evidence_citations ARRAY<STRING>,
  critic_score FLOAT64,
  human_sign_off_status STRING,
  signed_by STRING,
  signed_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL
)
PARTITION BY DATE(created_at)
CLUSTER BY str_reference_no, case_id;
