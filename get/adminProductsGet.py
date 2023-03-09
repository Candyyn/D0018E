import json

from db.basket import getBasket
from db.user import getUser, checkIfAuth, hasPermission, getUsers
from db.products import getProducts


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        try:
            user = checkIfAuth(request)
            hasPermission(user, 0x01010000)
            products = getProducts(0)
            return json.dumps({'products': products}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
