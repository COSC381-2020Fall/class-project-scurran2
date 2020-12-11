from http.server import BaseHTTPRequestHandler, HTTPServer

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
# self is instance of class (like this in java). In this case web server instance
    def do_GET(self):
        self.send_response(200) #"no problems" response
        self.send_header("Content-type", "text/html")
        self.end_headers()

        #dynamically generate webpage
        self.wfile.write(b"<!DOCTYPE html>")
        self.wfile.write(b"<html lang = 'en'>")
        self.wfile.write(b"<head>")
        self.wfile.write(b"<title>hello, title </title>");
        self.wfile.write(b"</head>") 
        
        self.wfile.write(b"<body>")
        self.wfile.write(b"Hello world!")
        self.wfile.write(b"</body>")
        self.wfile.write(b"</html>")   

port = 5000
# 0.0.0.0 means all IP v4 addresses on local machine 
# i.e. if host (e.g. aws machine) has 2 ip addresses, 
# server is reachable on both
server_address = ("0.0.0.0", port)
#server_address = ("127.0.0.1", port)
httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
httpd.serve_forever()