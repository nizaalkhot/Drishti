"""
Drishti BigQuery Export Service.
Streams scored transactions, risk events, and STR dossiers directly to
Google Cloud BigQuery (drishti_fraud_lake dataset) for transaction and risk analytics,
with an in-memory audit journal fallback for local development and offline runs.
"""
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

logger = logging.getLogger("drishti.bigquery_export")

try:
    from google.cloud import bigquery
    from google.api_core.exceptions import GoogleAPIError
    HAVE_BIGQUERY = True
except ImportError:
    HAVE_BIGQUERY = False

class BigQueryExportService:
    def __init__(self, project_id: Optional[str] = None, dataset_id: str = "drishti_fraud_lake"):
        self.project_id = project_id or os.getenv("GCP_PROJECT", "team-gain")
        self.dataset_id = dataset_id
        self.transactions_table = f"{self.project_id}.{self.dataset_id}.transaction_risk_events"
        self.dossiers_table = f"{self.project_id}.{self.dataset_id}.filed_dossiers"
        
        self.bq_client = None
        self._local_transaction_journal: List[Dict[str, Any]] = []
        self._local_dossier_journal: List[Dict[str, Any]] = []

        if HAVE_BIGQUERY and (os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("K_SERVICE")):
            try:
                self.bq_client = bigquery.Client(project=self.project_id)
                logger.info(f"BigQueryExportService connected to Google Cloud project: {self.project_id}")
            except Exception as e:
                logger.warning(f"Failed to initialize live BigQuery client: {e}. Using local journal fallback.")
                self.bq_client = None
        else:
            logger.info("BigQueryExportService operating in local offline fallback journal mode.")

    def export_transaction_risk(self, risk_event: Dict[str, Any]) -> bool:
        """
        Streams a scored transaction risk event to BigQuery.
        """
        payload = dict(risk_event)
        if "inserted_at" not in payload:
            payload["inserted_at"] = datetime.now(timezone.utc).isoformat()

        # Always record in local journal for queryability and audits
        self._local_transaction_journal.append(payload)

        if self.bq_client:
            try:
                is_synthetic = payload.get("is_synthetic", False)
                target_table = f"{self.transactions_table}_sandbox" if is_synthetic else self.transactions_table
                errors = self.bq_client.insert_rows_json(target_table, [payload])
                if errors:
                    logger.error(f"BigQuery streaming insert errors: {errors}")
                    return False
                logger.info(f"Successfully streamed risk event {payload.get('txn_id')} to BigQuery table {target_table}")
                return True
            except Exception as e:
                logger.warning(f"BigQuery stream failed ({e}), retained in local journal.")
                return False
        return True

    def export_filed_dossier(self, dossier: Dict[str, Any]) -> bool:
        """
        Streams a filed FIU-IND STR dossier to BigQuery for central compliance intelligence.
        """
        payload = dict(dossier)
        if "inserted_at" not in payload:
            payload["inserted_at"] = datetime.now(timezone.utc).isoformat()

        self._local_dossier_journal.append(payload)

        if self.bq_client:
            try:
                errors = self.bq_client.insert_rows_json(self.dossiers_table, [payload])
                if errors:
                    logger.error(f"BigQuery dossier stream errors: {errors}")
                    return False
                logger.info(f"Successfully streamed STR dossier {payload.get('case_id')} to BigQuery table {self.dossiers_table}")
                return True
            except Exception as e:
                logger.warning(f"BigQuery dossier stream failed ({e}), retained in local journal.")
                return False
        return True

    def get_local_transactions(self) -> List[Dict[str, Any]]:
        return list(self._local_transaction_journal)

    def get_local_dossiers(self) -> List[Dict[str, Any]]:
        return list(self._local_dossier_journal)

default_bq_export = BigQueryExportService()
