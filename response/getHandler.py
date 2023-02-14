from response.requestHandler import RequestHandler
from importlib import import_module
import sys
import importlib.util


class PostHandler(RequestHandler):
    request = None

    def __init__(self, request):
        self.request = request
        super().__init__()
        self.contentType = 'text/json'

    def find(self, routeData, routeArgs):
        try:

            # convert an array of string like test=123 to a dict like {'test': '123'}
            route_args = dict([arg.split('=') for arg in routeArgs])
            spec = importlib.util.spec_from_file_location("get", 'get/{}'.format(routeData['post']))
            foo = importlib.util.module_from_spec(spec)
            sys.modules["get"] = foo
            spec.loader.exec_module(foo)
            _postClass = foo.PostClass()
            self.setStatus(200)
            data = _postClass.exec(self, self.request, route_args)
            self.contents = data
            return True
        except Exception as e:
            self.setStatus(404)
            return False
