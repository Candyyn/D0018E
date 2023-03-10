from response.requestHandler import RequestHandler
from importlib import import_module
import sys
import importlib.util


class DeleteHandler(RequestHandler):
    request = None

    def __init__(self, request):
        self.data_string = request.data_string
        self.request = request
        super().__init__()
        self.contentType = 'text/json'

    def find(self, routeData, routeArgs):
        try:

            # convert an array of string like test=123 to a dict like {'test': '123'}
            route_args = dict([arg.split('=') for arg in routeArgs])
            spec = importlib.util.spec_from_file_location("delete", 'delete/{}'.format(routeData['delete']))
            foo = importlib.util.module_from_spec(spec)
            sys.modules["delete"] = foo
            spec.loader.exec_module(foo)
            _deleteClass = foo.DeleteClass()
            self.setStatus(200)
            data = _deleteClass.exec(self, self.request, route_args)
            self.contents = data
            return True
        except Exception as e:
            print(e)
            self.setStatus(404)
            return False
