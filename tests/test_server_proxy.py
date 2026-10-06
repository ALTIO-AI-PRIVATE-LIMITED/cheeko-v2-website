"""The local preview must forward website demo requests to the Manager API."""

import io
import unittest
from unittest.mock import patch

import server


class FakeResponse:
    status = 200
    headers = {"Content-Type": "application/json"}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return b'{"code":0,"data":{"token":"website-token"}}'


class FakeHandler(server.WebsiteHandler):
    path = "/api/web-demo/auth/google"
    command = "POST"
    headers = {"Content-Length": "0", "Content-Type": "application/json", "Authorization": "Bearer firebase-id-token"}
    rfile = io.BytesIO()
    wfile = io.BytesIO()

    def __init__(self):
        self.response_status = None
        self.response_headers = {}

    def send_response(self, status):
        self.response_status = status

    def send_header(self, name, value):
        self.response_headers[name] = value

    def end_headers(self):
        pass


class LocalProxyTests(unittest.TestCase):
    def test_google_post_forwards_method_path_and_token(self):
        handler = FakeHandler()
        with patch.dict("os.environ", {"CHEEKO_MANAGER_API_URL": "http://127.0.0.1:8002"}):
            with patch("server.urlopen", return_value=FakeResponse()) as urlopen:
                server.WebsiteHandler.do_POST(handler)

        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "http://127.0.0.1:8002/toy/web-demo/auth/google")
        self.assertEqual(request.get_method(), "POST")
        self.assertIsNone(request.data)
        self.assertEqual(request.get_header("Authorization"), "Bearer firebase-id-token")
        self.assertEqual(handler.response_status, 200)
        self.assertIn(b'"token":"website-token"', handler.wfile.getvalue())

    def test_session_delete_forwards_authorization(self):
        handler = FakeHandler()
        handler.command = "DELETE"
        handler.path = "/api/web-demo/voice/11111111-2222-4333-8444-555555555555"
        handler.headers = {"Authorization": "Bearer demo-token", "Content-Length": "0"}
        with patch("server.urlopen", return_value=FakeResponse()) as urlopen:
            server.WebsiteHandler.do_DELETE(handler)

        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "DELETE")
        self.assertEqual(request.get_header("Authorization"), "Bearer demo-token")


if __name__ == "__main__":
    unittest.main()
