import os
import urllib.parse
from http.server import BaseHTTPRequestHandler

from routes.main import routes

from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.postHandler import PostHandler


class Server(BaseHTTPRequestHandler):
    data_string = None

    def getAuthToken(self):
        try:
            return self.headers['Authorization']
        except:
            return None

    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        request_path = self.path.split('?')[0]
        try:
            request_args = split_path[0].split('?')[1]
            request_args = request_args.split('&')

            temp = self.rfile.read(int(self.headers['Content-Length']))
            self.data_string = temp.decode('utf-8').split('&')
        except:
            request_args = ""

        if request_extension == "" or request_extension == ".html":
            if request_path in routes:
                handler = TemplateHandler(self)
                handler.find(routes[request_path], request_args)
            else:
                handler = BadRequestHandler()
        elif request_extension == ".py":
            handler = BadRequestHandler()
        else:
            handler = StaticHandler()
            handler.find(request_path)

        self.respond({
            'handler': handler
        })

    def checkifAfterSymbol(self, my_string, symbol, target):
        if symbol in my_string:
            substrings = my_string.split(symbol)
            if target in substrings[1]:
                return True
            else:
                return False
        else:
            return False

    # Create a list with whitelisted extensions
    def do_POST(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]

        if self.checkifAfterSymbol(self.path, '?', request_extension):
            split_path = (split_path[0] + request_extension, "")
            request_extension = ""

        request_path = self.path.split('?')[0]
        try:
            request_args = split_path[0].split('?')[1]
            request_args = request_args.split('&')

        except:
            request_args = ""

        try:
            temp = self.rfile.read(int(self.headers['Content-Length']))
            self.data_string = {s.split('=')[0]: s.split('=')[1] for s in urllib.parse.unquote(temp.decode('utf-8')).split('&')}
        except:
            self.data_string = ""

        if request_extension == "" or request_extension == ".html":
            if request_path in routes:
                handler = PostHandler(self)
                handler.find(routes[request_path], request_args)
            else:
                handler = BadRequestHandler()
        else:
            handler = BadRequestHandler()

        self.respond({
            'handler': handler
        })

    def handle_http(self, handler):
        status_code = handler.getStatus()

        self.send_response(status_code)

        content = handler.getContents()
        self.send_header('Content-type', handler.getContentType())

        if status_code == 404:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')

    def respond(self, opts):
        try:
            response = self.handle_http(opts['handler'])
            self.wfile.write(response)
        except ConnectionAbortedError:
            pass
