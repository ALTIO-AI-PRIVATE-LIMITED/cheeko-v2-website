"""Local website preview with the same demo API path used on Netlify."""

import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
API_PREFIX = "/api/web-demo/"
MAX_REQUEST_BYTES = 64 * 1024


class WebsiteHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.startswith(API_PREFIX):
            self._proxy()
        else:
            super().do_GET()

    def do_POST(self):
        self._proxy()

    def do_DELETE(self):
        self._proxy()

    def _proxy(self):
        path = urlsplit(self.path)
        if not path.path.startswith(API_PREFIX):
            self.send_error(404, "Not found")
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_error(400, "Invalid request length")
            return
        if size < 0 or size > MAX_REQUEST_BYTES:
            self.send_error(413, "Request too large")
            return

        body = self.rfile.read(size) if size else None
        manager = os.environ.get("CHEEKO_MANAGER_API_URL", "http://127.0.0.1:8002").rstrip("/")
        target = manager + "/toy/web-demo/" + self.path[len(API_PREFIX):]
        headers = {"Content-Type": self.headers.get("Content-Type", "application/json")}
        if self.headers.get("Authorization"):
            headers["Authorization"] = self.headers["Authorization"]
        request = Request(target, data=body, headers=headers, method=self.command)

        try:
            with urlopen(request, timeout=15) as response:
                self._send_api_response(response.status, response.read(), response.headers)
        except HTTPError as error:
            self._send_api_response(error.code, error.read(), error.headers)
        except URLError:
            self._send_api_response(502, json.dumps({
                "code": 502,
                "msg": "Local Cheeko Manager API is unavailable. Start it on port 8002, then try again.",
                "data": None,
            }).encode("utf-8"), {"Content-Type": "application/json"})

    def _send_api_response(self, status, body, headers):
        self.send_response(status)
        self.send_header("Content-Type", headers.get("Content-Type", "application/json"))
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("CHEEKO_SITE_PORT", "8123"))
    print(f"Cheeko site → http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), WebsiteHandler).serve_forever()
