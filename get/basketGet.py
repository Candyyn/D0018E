import json

from db.basket import getBasket
from db.user import getUser


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        # Get User basket from token
        # _user = getUser(request.headers['authorization'])
        _token = request.headers['authorization']
        if _token is None:
            return json.dumps({'error': 'Not Authorized'}, default=str)
        token = _token.split(' ')[1]
        user = getUser(token)
        basket = getBasket(user['id'])

        return json.dumps({'basket': basket}, default=str)
