"""Tier 0, and the daily spend counter that shares its table.

Questionnaire rows get copy-pasted between companies endlessly, so the same
row arrives again and again with different numbering and whitespace. The
normaliser collapses those into one hash, and a hit costs one DynamoDB read
and zero model calls.

The same table carries the daily spend counter. AWS Budgets tells you after
the money is gone; this is what actually stops it. The counter is incremented
before the expensive work rather than after, so a burst of concurrent requests
cannot all pass the check and then all spend.

    PK                  SK        payload
    CACHE#<sha256>      VERDICT   rendered verdict, with a ttl
    SPEND#2026-08-26    COUNTER   model calls and rough token count today
"""
import datetime
import json
import os

from .schema import Verdict


class MemoryCache:
    """Local and test use. Also what the Lambda falls back to if DynamoDB is
    unreachable, because a cache being down should slow the agent, not break
    it."""

    def __init__(self):
        self._store = {}
        self.hits = 0
        self.misses = 0

    def get(self, key):
        value = self._store.get(key)
        if value is None:
            self.misses += 1
            return None
        self.hits += 1
        return Verdict.model_validate(json.loads(value))

    def put(self, key, verdict):
        self._store[key] = verdict.model_dump_json()

    def spend_today(self):
        return self._store.get("__spend__", 0)

    def add_spend(self, calls=1):
        self._store["__spend__"] = self.spend_today() + calls
        return self._store["__spend__"]


class DynamoCache:
    """One table, on-demand billing, no indexes.

    Every failure path here degrades rather than raises. A verdict that took a
    model call to produce is still a correct verdict if we then fail to store
    it, and an agent that returns 500 because a cache write failed is worse
    than one that is briefly slower.
    """

    def __init__(self, table_name=None, region=None, ttl_days=30, client=None):
        self.table_name = table_name or os.environ.get("WHYF_TABLE", "whyf")
        self.ttl_days = ttl_days
        self.hits = 0
        self.misses = 0
        self.errors = 0
        if client is not None:
            self._table = client
        else:
            import boto3
            self._table = boto3.resource(
                "dynamodb", region_name=region).Table(self.table_name)

    # ---- verdict cache ---------------------------------------------------

    def get(self, key):
        try:
            item = self._table.get_item(
                Key={"PK": "CACHE#" + key, "SK": "VERDICT"}).get("Item")
        except Exception:
            self.errors += 1
            return None
        if not item:
            self.misses += 1
            return None
        self.hits += 1
        try:
            return Verdict.model_validate(json.loads(item["payload"]))
        except Exception:
            # A payload written by an older schema is a miss, not a crash.
            self.errors += 1
            return None

    def put(self, key, verdict):
        expires = int((datetime.datetime.now(datetime.timezone.utc)
                       + datetime.timedelta(days=self.ttl_days)).timestamp())
        try:
            self._table.put_item(Item={
                "PK": "CACHE#" + key,
                "SK": "VERDICT",
                "payload": verdict.model_dump_json(),
                "concept": verdict.concept or "none",
                "ttl": expires,
            })
        except Exception:
            self.errors += 1

    # ---- daily spend counter ---------------------------------------------

    def _today(self):
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    def spend_today(self):
        try:
            item = self._table.get_item(
                Key={"PK": "SPEND#" + self._today(), "SK": "COUNTER"}).get("Item")
        except Exception:
            self.errors += 1
            return 0
        return int(item.get("model_calls", 0)) if item else 0

    def add_spend(self, calls=1):
        """Atomic increment, and it happens before the spend rather than after.
        Under concurrency the alternative is every request reading the same
        under-limit value and then all of them spending."""
        try:
            response = self._table.update_item(
                Key={"PK": "SPEND#" + self._today(), "SK": "COUNTER"},
                UpdateExpression="ADD model_calls :n SET #t = :ttl",
                ExpressionAttributeNames={"#t": "ttl"},
                ExpressionAttributeValues={
                    ":n": calls,
                    ":ttl": int((datetime.datetime.now(datetime.timezone.utc)
                                 + datetime.timedelta(days=45)).timestamp()),
                },
                ReturnValues="UPDATED_NEW")
            return int(response["Attributes"]["model_calls"])
        except Exception:
            self.errors += 1
            # Failing open on the counter would be the expensive mistake, so
            # report the ceiling and let the caller degrade.
            return None

    def stats(self):
        total = self.hits + self.misses
        return {"hits": self.hits, "misses": self.misses,
                "hit_rate": (self.hits / total) if total else 0.0,
                "errors": self.errors}
