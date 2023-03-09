from db.main import Database
from db.test import Test
import json
from db.user import registerUser


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        if len(args) != 6:
            posthandler.setStatus(400)
            posthandler.contentType = 'text/json'
            return json.dumps({'error': "Invalid Arguments"})

        data, token = registerUser(args['email'], args['password'], args['first_name'], args['last_name'], args['phone'], args['address'])

        if token is not None:
            posthandler.setStatus(200)
            posthandler.contentType = 'text/json'
            return json.dumps({'user': data, 'token': token})
        else:
            posthandler.setStatus(401)
            posthandler.contentType = 'text/json'
            return json.dumps({'error': "Error Registering User"})
