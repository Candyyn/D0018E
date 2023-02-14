from db.main import Database
from db.test import Test
import json
from db.user import loginUser


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        token = loginUser(args['email'], args['password'])
        if token is not None:
            print(token)
            posthandler.setStatus(200)
            posthandler.contentType = 'text/json'
            return json.dumps({'token': token})
        else:
            posthandler.setStatus(401)
            posthandler.contentType = 'text/json'
            return json.dumps({'error': "Invalid Email or Password"})
