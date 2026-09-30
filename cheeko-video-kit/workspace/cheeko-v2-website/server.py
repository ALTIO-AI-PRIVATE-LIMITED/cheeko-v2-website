import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Cheeko site → http://127.0.0.1:8123")
HTTPServer(("127.0.0.1", 8123), SimpleHTTPRequestHandler).serve_forever()
