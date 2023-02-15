import json

from db.user import getUser, checkIfAuth
from db.basket import addBasket


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        # Get User basket from token
        try:
            user = checkIfAuth(request)
            product_id = args['product_id']
            addBasket(user['id'], product_id)
            return json.dumps({'success': True}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
