#! /usr/bin/python

import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        result = {
            'result': socket.gethostbyname('example.com'),
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))


if __name__ == '__main__':
    try:
        server = HTTPServer(('', 8080), RequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        pass
