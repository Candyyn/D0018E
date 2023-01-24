import os

from http.server import BaseHTTPRequestHandler

from routes.main import routes

from response.staticHandler import StaticHandler
from response.templateHandler import TemplateHandler
from response.badRequestHandler import BadRequestHandler
from response.postHandler import PostHandler


class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        request_path = self.path.split('?')[0]
        try:
            request_args = split_path[0].split('?')[1]
            request_args = request_args.split('&')
        except:
            request_args = ""

        if request_extension == "" or request_extension == ".html":
            if request_path in routes:
                handler = TemplateHandler()
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

    def do_POST(self):
        split_path = os.path.splitext(self.path)
        request_extension = split_path[1]
        request_path = self.path.split('?')[0]
        try:
            request_args = split_path[0].split('?')[1]
            request_args = request_args.split('&')
        except:
            request_args = ""

        if request_extension == "" or request_extension == ".html":
            if request_path in routes:
                handler = PostHandler()
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

        if status_code == 200:
            content = handler.getContents()
            self.send_header('Content-type', handler.getContentType())
        else:
            content = "404 Not Found"

        self.end_headers()

        if isinstance(content, bytes):
            return content
        else:
            return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['handler'])
        self.wfile.write(response)