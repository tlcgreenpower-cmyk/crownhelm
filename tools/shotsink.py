# -*- coding: utf-8 -*-
"""Catch TFshot() data URLs from the game and write them to disk as real JPEGs.

The game can photograph itself (b252) but the picture had nowhere to go: pulling a 60,000-character
data URL back through a tool result costs more than it is worth. This listens on 8138, takes a POST
of the data URL, and drops the decoded image in the scratchpad where the Read tool can open it.
"""
import base64, os, http.server

OUT = os.path.dirname(os.path.abspath(__file__))


class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n).decode("utf-8", "replace")
        name = (self.path.strip("/") or "shot") + ".jpg"
        raw = body.split(",", 1)[1] if body.startswith("data:") else body
        path = os.path.join(OUT, name)
        with open(path, "wb") as f:
            f.write(base64.b64decode(raw))
        self.send_response(200); self._cors()
        self.send_header("Content-Type", "text/plain"); self.end_headers()
        self.wfile.write(("%s %d bytes" % (path, os.path.getsize(path))).encode())

    def log_message(self, *a):
        pass


http.server.HTTPServer(("127.0.0.1", 8138), H).serve_forever()
