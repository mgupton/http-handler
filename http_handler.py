#
# Written by: Michael Gupton
#
# HTTP Handler is a simple HTTP server that provides
# a basic framework for handling HTTP requests.
#
# The server is implemented to support multi-threading,
# so that multiple requests can be handled concurrently.
#
# This is a minimalist script that reflects or echoes the requests from
# HTTP methods GET, POST, PUT, and DELETE to the screen and back to
# the user-agent/client that sent the data.
#
# One use of this program is for testing webhooks.
#
#
# Example Usage:
#
# To use HTTP, as opposed to HTTPS.
#
# python http_handler.py
#
# To use this script to handle requests over SSL/TLS.
#
# python http_handler.py -s -p 443 --cert cert.pem --key key.pem
#
#
# To test the server make curl requests like the following.
#
# curl -X POST -d "Hello World!" http://<host address>
#
# curl -X POST -d "Hello World!" http://localhost
#
# curl -X POST -H "Content-Type: application/json" -d '{"fname": "scrappy"}' http://localhost
#
#
# Multithreaded server example:
#
# https://github.com/Nakiami/MultithreadedSimpleHTTPServer
#

#
#
# The following imports work for Python 2.x.
#
# from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

try:
    # Python 2.x
    from SocketServer import ThreadingMixIn
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from BaseHTTPServer import HTTPServer

except ImportError:
    # Python 3.x
    from socketserver import ThreadingMixIn
    from http.server import SimpleHTTPRequestHandler, HTTPServer

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass
    
# The following imports work for Python 3.x.
from http.server import BaseHTTPRequestHandler

import ssl
import argparse
import sys
import json

import pdb

def main(args):
    
    port = args.p
    
    print('Listening on port %s' % port)
    
    # server = HTTPServer(('0.0.0.0', port), RequestHandler)
    
    server = ThreadingSimpleServer(('', port), RequestHandler)    

#
# If the option to enable SSL/TLS is on then setup the socket accordingly.
#    
    if args.https == True:
    
        server.socket = ssl.wrap_socket(server.socket,
            server_side=True,
            certfile=args.cert,
            keyfile=args.key)   
    
    # server.serve_forever()
    
    while True:
    
        try:
    
            server.handle_request()
            
            print("Handling request", file=sys.stderr)
            
        except KeyboardInterrupt as e:
        
            print("Exiting")
    

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        print(self.headers)
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_POST(self):
        
        request_path = self.path
        
        print("\n----- Request Start ----->\n")
        print(request_path)
        
        request_headers = self.headers
        content_length = request_headers.get('content-length')
        length = int(content_length)
        
        # pdb.set_trace()
        
        print(request_headers)
        
        post_data = self.rfile.read(length)
        
        print(post_data.decode("utf-8"))
        
        if "json" in request_headers.get('content-type'):
        
            print("JSON received")
        
            json_text = json.loads(post_data.decode("utf-8"))
        
            # print(json_text["fname"])
        
        
        print("<----- Request End -----\n")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Echo the post data back to the client.
        self.wfile.write(post_data)
    
    do_PUT = do_POST
    do_DELETE = do_GET

    
        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
       
    parser.add_argument('-p', action='store', type=int, default=80, required=False, help="port to listen on")
    
    parser.add_argument('--cert', action='store', type=str, required=False, help="SSL/TLS certificate")
    
    parser.add_argument('--key', action='store', type=str, required=False, help="private key for certificate")
    
    parser.add_argument('-s', '--https', action='store_true', default=False, help='use https')    
    
    args = parser.parse_args()
    
    main(args)
    

    
    
