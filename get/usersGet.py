import json

from db.basket import getBasket
from db.user import getUser, checkIfAuth, hasPermission


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        # Get User basket from token
        # _user = getUser(request.headers['authorization'])
        try:
            user = checkIfAuth(request)
            hasPermission(user, 0x01100000)
            basket = getBasket(user['id'])
            return json.dumps({'basket': basket}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
