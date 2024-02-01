import hmac
from hashlib import sha1
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from modules import settings, parser


class Listener(BaseHTTPRequestHandler):
    def _write(self, content: str, status: int=200):
        self.send_response(status)
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if (("hub.challenge" in query) and ("hub.verify_token" in query)
                and (query["hub.verify_token"][0] == settings.get("VERIFY_TOKEN"))):
            self._write(query["hub.challenge"][0])
            print("* GET Verified.")
        else:
            self._write("Invalid token.", 404)
            print("* GET Rejected.")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        signature = self.headers.get('X-Hub-Signature', '')
        secret = settings.get("VERIFY_TOKEN").encode('utf-8')
        digest = hmac.new(secret, body, sha1).hexdigest()
        computed_signature = "sha1=" + digest

        if signature != computed_signature:
            self._write("HMAC signature mismatch.")
            print("* POST Rejected.")
            return

        self._write("OK")
        parser.parse_feed(body.decode('utf-8'))
        print("* POST Verified.")


def run_server():
    addr = settings.get("LISTENER_ADDR")
    port = settings.get("LISTENER_PORT")
    httpd = ThreadingHTTPServer((addr, port), Listener)
    httpd.serve_forever()
