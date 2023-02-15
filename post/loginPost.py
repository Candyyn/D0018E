from db.main import Database
from db.test import Test
import json
from db.user import loginUser


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        if len(args) != 2:
            if len(posthandler.data_string) != 2:
                posthandler.setStatus(400)
                posthandler.contentType = 'text/json'
                return json.dumps({'error': "Invalid Arguments"})
            else:
                args = posthandler.data_string
        data, token = loginUser(args['email'], args['password'])
        "token = None"
        if token is not None:
            posthandler.setStatus(200)
            posthandler.contentType = 'text/json'
            return json.dumps({'user': data, 'token': token})
        else:
            posthandler.setStatus(401)
            posthandler.contentType = 'text/json'
            return json.dumps({'error': "Invalid Email or Password"})
