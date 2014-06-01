__author__ = 'Link'
from http.server import HTTPServer, SimpleHTTPRequestHandler

HTTPServer(("0.0.0.0", 8080), SimpleHTTPRequestHandler).serve_forever()