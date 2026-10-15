"""Distributed sliding-window velocity tracking backed by Redis (Google Cloud Memorystore).

Uses Redis Sorted Sets (ZSET) for atomic, sub-millisecond sliding window velocity
checks across horizontally autoscaling Cloud Run instances.
"""

import logging
from datetime import datetime
from typing import Tuple, Optional, Union

logger = logging.getLogger("drishti.velocity.redis")

class RedisVelocityCache:
    """Production Redis-backed sliding-window velocity cache for sender accounts."""

    def __init__(self, redis_url: str):
        try:
            import redis
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self._available = True
            logger.info("Initialized RedisVelocityCache with endpoint: %s", redis_url)
        except Exception as e:
            logger.warning("Failed to initialize Redis client (%s); falling back to in-memory mode.", e)
            self.redis_client = None
            self._available = False

    def is_available(self) -> bool:
        return self._available and self.redis_client is not None

    def _to_timestamp(self, ts: Union[datetime, float, int]) -> float:
        if isinstance(ts, datetime):
            return ts.timestamp()
        return float(ts)

    def record(self, sender_id: str, timestamp: Union[datetime, float, int], amount: float) -> None:
        """Records a transaction in the sender's velocity sorted set with a 24-hour TTL."""
        if not self.is_available():
            return

        timestamp_s = self._to_timestamp(timestamp)
        key = f"vel:{sender_id}"
        member = f"{timestamp_s}:{amount}"
        one_day_ago = timestamp_s - 86400

        try:
            pipe = self.redis_client.pipeline(transaction=True)
            # Add entry with timestamp as score
            pipe.zadd(key, {member: timestamp_s})
            # Prune entries older than 24 hours
            pipe.zremrangebyscore(key, "-inf", one_day_ago)
            # Set key expiration to 24h
            pipe.expire(key, 86400)
            pipe.execute()
        except Exception as e:
            logger.warning("Redis velocity record error for sender %s: %s", sender_id, e)

    def get_velocity(self, sender_id: str, current_time: Union[datetime, float, int]) -> Tuple[int, float, int]:
        """Calculates sliding window velocities: (1h_count, 1h_amount, 24h_count)."""
        if not self.is_available():
            return 0, 0.0, 0

        current_time_s = self._to_timestamp(current_time)
        key = f"vel:{sender_id}"
        one_hour_ago = current_time_s - 3600
        one_day_ago = current_time_s - 86400

        try:
            # Query all entries within the last 24 hours
            entries = self.redis_client.zrangebyscore(key, one_day_ago, "+inf")
            v1_count = 0
            v1_amount = 0.0
            v24_count = len(entries)

            for entry in entries:
                try:
                    ts_str, amt_str = entry.split(":", 1)
                    ts = float(ts_str)
                    amt = float(amt_str)
                    if ts >= one_hour_ago:
                        v1_count += 1
                        v1_amount += amt
                except ValueError:
                    continue

            return v1_count, v1_amount, v24_count
        except Exception as e:
            logger.warning("Redis velocity read error for sender %s: %s", sender_id, e)
            return 0, 0.0, 0
