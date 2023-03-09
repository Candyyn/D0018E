import json

from db.basket import getBasket
from db.user import getUser, checkIfAuth, hasPermission, getUsers
from db.orders import getOrders


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        try:
            user = checkIfAuth(request)
            # hasPermission(user, 0x01110000)
            # Implement order table
            return json.dumps({'orders': getOrders()}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
