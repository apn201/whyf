"""Run the whole thing locally: the agent behind an HTTP endpoint, and the PWA.

The same handler the Lambda uses, so what you see here is what deploys.

    python tools/serve_local.py --profile whyf
    open http://localhost:8000

Needs AWS credentials because the classifier and the embedding call are real
Bedrock. Everything else is local: the cards, the lexical index, the cache.
"""
import argparse
import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "web"
sys.path.insert(0, str(ROOT / "src"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(WEB), **kw)

    def log_message(self, fmt, *args):
        if "POST" in (args[0] if args else ""):
            sys.stderr.write("  " + fmt % args + "\n")

    def do_GET(self):
        """Serve the page, pointed at this server rather than at production.

        index.html carries the deployed Function URL as its default, so that
        opening the file on its own talks to the real thing. That default is
        wrong here: the whole point of this script is to exercise the agent on
        this machine. Injecting window.WHYF_API ahead of the page's own script
        overrides it without either copy of the file needing to know about the
        other.
        """
        if self.path.split("?")[0] not in ("/", "/index.html"):
            return super().do_GET()

        page = (WEB / "index.html").read_text(encoding="utf-8")
        shim = "<script>window.WHYF_API = location.origin;</script>"
        marker = "<script>"
        page = page.replace(marker, shim + marker, 1) if marker in page             else shim + page

        payload = page.encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header("access-control-allow-origin", "*")
        self.send_header("access-control-allow-headers", "content-type")
        self.send_header("access-control-allow-methods", "POST,OPTIONS")

    def do_POST(self):
        from whyf.handler import handler as lambda_handler

        length = int(self.headers.get("content-length") or 0)
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        event = {
            "rawPath": self.path.split("?")[0],
            "requestContext": {"http": {"method": "POST"}},
            "body": body,
        }
        result = lambda_handler(event)

        payload = result["body"].encode("utf-8")
        self.send_response(result["statusCode"])
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self._cors()
        self.end_headers()
        self.wfile.write(payload)

        try:
            v = json.loads(result["body"])
            t = v.get("telemetry") or {}
            print("    -> {} | {} | {} calls | {:.2f}s".format(
                v.get("verdict") or v.get("question_class"),
                t.get("tier"), t.get("model_calls", 0), t.get("elapsed_s", 0)))
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=None)
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()

    if args.profile:
        os.environ["AWS_PROFILE"] = args.profile

    # Warm the pipeline before the first request so the browser does not wait
    # for eighty cards and eighty vectors to load.
    print("loading cards and index...")
    from whyf.handler import _pipeline
    pipeline = _pipeline()
    print("  {} concepts ready".format(len(pipeline.library.concepts)))

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print("\n  http://localhost:{}/?api=http://localhost:{}\n".format(
        args.port, args.port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    sys.exit(main())
