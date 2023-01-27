from db.main import Database
from db.user import User
import json


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):

        try:
            _user = User(request.headers['authorization'])
        except KeyError:
            posthandler.setStatus(401)
            return "Not logged in"
        return json.dumps(_user.raw, default=str)
