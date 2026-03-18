import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


def get_info():
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip = "unknown"
    return {
        "hostname": hostname,
        "ip": ip,
        "platform": os.uname().sysname,
        "environment": dict(os.environ),
    }


class WhoAmIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        info = get_info()
        body = json.dumps(info, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), WhoAmIHandler)
    print(f"Listening on port {port}...")
    server.serve_forever()
