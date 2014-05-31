__author__ = 'Link'
from http.server import HTTPServer, SimpleHTTPRequestHandler

HTTPServer(("192.168.1.3", 80), SimpleHTTPRequestHandler).serve_forever()