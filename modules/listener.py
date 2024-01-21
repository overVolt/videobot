from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from modules import settings

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
        else:
            self._write("Not found.", 404)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        print(body.decode('utf-8'))
        self._write("OK")


def run_server():
    addr = settings.get("LISTENER_ADDR")
    port = settings.get("LISTENER_PORT")
    httpd = ThreadingHTTPServer((addr, port), Listener)
    httpd.serve_forever()
