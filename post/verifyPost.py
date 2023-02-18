import json

from db.user import getUser, verifyToken


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):

        # remove Bearer from token
        token = request.headers['authorization'].replace("Bearer ", "")

        response = verifyToken(token)
        return json.dumps({'tokenVerified': response}, default=str)
