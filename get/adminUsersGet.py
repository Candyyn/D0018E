import json

from db.basket import getBasket
from db.user import getUser, checkIfAuth, hasPermission, getUsers


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        try:
            user = checkIfAuth(request)
            hasPermission(user, 0x01100000)
            users = getUsers()
            return json.dumps({'users': users}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
