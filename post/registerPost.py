from db.main import Database
from db.test import Test
import json
from db.user import registerUser


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        print(registerUser(args['email'], args['password'], "test", "test123"))
        print(args)
        return "test"
