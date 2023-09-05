#!/usr/bin/env python3
# *_* coding: utf-8 *_*
"""HTTP server that reflects HTTP headers"""

import http.server
import html
import argparse

DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 8099

class Reflector(http.server.BaseHTTPRequestHandler):
    """RequestHandler that displays all headers sent as part of GET requests"""
    def do_GET(self) -> None:
        """Responds to any HTTP GET request with a page showing the headers sent to the server"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        body_text = "<body><h1>Response headers:</h1><pre>" + html.escape(str(self.headers)) + "</pre></body>"
        self.wfile.write(bytes(body_text, "utf8"))

def launch_server(addr: str, port: int, Handler: Reflector) -> None:
    """Launches the reflection server on the specified IP and port

    Args:
        addr (str): IP address the server will bind to
        port (int): port the server will listen on
        Handler (Reflector): HTTP Handler class that handles GET requests
    """
    web_server = http.server.HTTPServer((addr, port), Handler)
    print("Connect to http://" + addr + ":" + str(port) + " to see headers. CTRL-C to quit.")
    web_server.serve_forever()

def parse_args():
    """Parses command line arguments to get the bind address and port

    Returns:
        _type_: tuple representing bind address and bind port
    """
    parser = argparse.ArgumentParser(description="HTTP server that reflects HTTP headers")
    parser.add_argument("-a", "--addr", help="IP address to bind to", default=DEFAULT_ADDR)
    parser.add_argument("-p", "--port", help="port to bind to", type=int, default=DEFAULT_PORT)
    args = parser.parse_args()
    return (args.addr, args.port)

if __name__ == "__main__":
    """Launches the server when started from the command line
    """
    addr, port = parse_args()
    launch_server(addr, port, Reflector)
