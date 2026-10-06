"""
Google Cloud Pub/Sub Event Streaming Service.
Streams high-throughput transaction events, real-time fraud alerts, and automated FIU-IND STR filings.
"""
import os
import json
import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timezone

logger = logging.getLogger("drishti.pubsub")

TOPIC_TRANSACTIONS = "drishti-transaction-events"
TOPIC_ALERTS = "drishti-fraud-alerts"
TOPIC_STR_FILINGS = "drishti-str-filings"

class DrishtiPubSubService:
    """
    Decoupled event messaging engine via Google Cloud Pub/Sub.
    Features live Cloud Pub/Sub publishing with in-memory resilient fallback.
    """
    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GCP_PROJECT", "team-gain")
        self._publisher = None
        self._local_subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {
            TOPIC_TRANSACTIONS: [],
            TOPIC_ALERTS: [],
            TOPIC_STR_FILINGS: []
        }
        self._published_history: List[Dict[str, Any]] = []

        try:
            from google.cloud import pubsub_v1
            self._publisher = pubsub_v1.PublisherClient()
            self._is_cloud_active = True
        except Exception as e:
            logger.info("Pub/Sub running in local resilient mode: %s", e)
            self._is_cloud_active = False

    def publish_event(self, topic_name: str, payload: Dict[str, Any]) -> str:
        """
        Publishes a JSON payload to a specified Google Cloud Pub/Sub topic.
        Returns message_id.
        """
        event_envelope = {
            "topic": topic_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": payload
        }
        self._published_history.append(event_envelope)

        # Notify any local in-process subscribers
        for sub in self._local_subscribers.get(topic_name, []):
            try:
                sub(payload)
            except Exception as e:
                logger.error("Local subscriber callback error: %s", e)

        if self._is_cloud_active and self._publisher:
            try:
                topic_path = self._publisher.topic_path(self.project_id, topic_name)
                data_bytes = json.dumps(event_envelope, default=str).encode("utf-8")
                future = self._publisher.publish(topic_path, data=data_bytes)
                return str(future.result())
            except Exception as e:
                logger.warning("Cloud Pub/Sub publish failed, recorded locally: %s", e)
        
        return f"LOCAL_MSG_{int(datetime.now(timezone.utc).timestamp()*1000)}"

    def publish_transaction_scored(self, scoring_data: Dict[str, Any]) -> str:
        return self.publish_event(TOPIC_TRANSACTIONS, scoring_data)

    def publish_fraud_alert(self, alert_data: Dict[str, Any]) -> str:
        return self.publish_event(TOPIC_ALERTS, alert_data)

    def publish_str_filing(self, str_data: Dict[str, Any]) -> str:
        return self.publish_event(TOPIC_STR_FILINGS, str_data)

    def subscribe_local(self, topic_name: str, callback: Callable[[Dict[str, Any]], None]):
        """Subscribes an in-process worker to a topic stream."""
        if topic_name in self._local_subscribers:
            self._local_subscribers[topic_name].append(callback)

    def subscribe(self, topic_name: str, callback: Callable[[Dict[str, Any]], None]):
        """Alias for subscribe_local."""
        self.subscribe_local(topic_name, callback)

    def get_published_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self._published_history[-limit:]

# Global singleton instance
default_pubsub_service = DrishtiPubSubService()
