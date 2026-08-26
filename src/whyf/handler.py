"""Lambda entry point, behind a Function URL.

Two routes, both POST, both tiny:

    POST /            {"question": "..."}                     -> verdict
    POST /answer      {"question","concept","option"}          -> flipped verdict

The Pipeline is built once at module scope so the cards, the lexical index and
the embedding vectors load on cold start and are reused by every warm
invocation. That is the whole reason tier 1 can be fast.
"""
import json
import os
import time

_PIPELINE = None
_COLD_START_MS = None


def _pipeline():
    """Built once per container. A failure here is fatal and should be, because
    an agent with no cards is not a degraded agent, it is a broken one."""
    global _PIPELINE, _COLD_START_MS
    if _PIPELINE is None:
        started = time.time()
        from .cache import DynamoCache, MemoryCache
        from .config import load
        from .pipeline import Pipeline

        config = load()
        try:
            cache = DynamoCache(table_name=config.table_name,
                                region=config.region,
                                ttl_days=config.limits.cache_ttl_days)
        except Exception:
            # No table yet, or no permission. Running without tier 0 is slower
            # and more expensive, not broken.
            cache = MemoryCache()
        _PIPELINE = Pipeline(config=config, cache=cache)
        _COLD_START_MS = (time.time() - started) * 1000
    return _PIPELINE


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "content-type": "application/json",
            # The demo URL is public and unauthenticated by design; it holds
            # nothing about anybody and needs no session.
            "access-control-allow-origin": os.environ.get("WHYF_ALLOW_ORIGIN", "*"),
            "access-control-allow-headers": "content-type",
            "access-control-allow-methods": "POST,OPTIONS",
            "cache-control": "no-store",
        },
        "body": json.dumps(body),
    }


def handler(event, context=None):
    method = (event.get("requestContext", {})
              .get("http", {}).get("method", "POST")).upper()
    if method == "OPTIONS":
        return _response(204, {})

    path = (event.get("rawPath") or "/").rstrip("/") or "/"

    try:
        payload = json.loads(event.get("body") or "{}")
    except (TypeError, ValueError):
        return _response(400, {"error": "body must be JSON"})

    question = (payload.get("question") or "").strip()
    if not question:
        return _response(400, {"error": "give me one row from a questionnaire"})
    if len(question) > 2000:
        # One row, not a whole column. Batch mode is a stretch goal and this is
        # also the cheapest possible denial-of-wallet guard.
        return _response(413, {"error": "that is longer than one question. "
                                        "Paste a single row."})

    try:
        pipeline = _pipeline()
        if path == "/answer":
            verdict = pipeline.answer(question,
                                      payload.get("concept"),
                                      payload.get("option"))
        else:
            verdict = pipeline.resolve(question)
    except Exception as exc:
        # Never leak a stack trace to a public URL. The logs have it.
        print("resolve failed: {}: {}".format(type(exc).__name__, exc))
        return _response(500, {"error": "could not answer that one"})

    body = json.loads(verdict.model_dump_json())
    if _COLD_START_MS:
        body.setdefault("telemetry", {})["cold_start_ms"] = round(_COLD_START_MS)
    return _response(200, body)
