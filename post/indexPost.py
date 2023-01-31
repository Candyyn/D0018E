from db.main import Database
from db.test import Test
import json


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        try:
            #_user = User(request.headers['authorization'])
            _users = Test("")
        except KeyError:
            posthandler.setStatus(401)
            return "Not logged in"
        return json.dumps(_users.array, default=str)
