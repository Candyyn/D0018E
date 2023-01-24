from response.requestHandler import RequestHandler
from importlib import import_module
import sys
import importlib.util


class PostHandler(RequestHandler):
    def __init__(self):
        super().__init__()
        self.contentType = 'text/json'

    def find(self, routeData, routeArgs):
        try:

            # convert an array of string like test=123 to a dict like {'test': '123'}
            route_args = dict([arg.split('=') for arg in routeArgs])
            print('post.{}'.format(routeData['post']))
            spec = importlib.util.spec_from_file_location("post", 'C:/Users/karle/WebstormProjects/D0018E/post/indexPost.py')
            foo = importlib.util.module_from_spec(spec)
            sys.modules["post"] = foo
            spec.loader.exec_module(foo)
            _postClass = foo.PostClass()
            data = _postClass.exec(route_args)
            self.contents = data
            self.setStatus(200)
            return True
        except Exception as e:
            print(e)
            self.setStatus(404)
            return False
