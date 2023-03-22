import json

from db.user import getUser, checkIfAuth
from db.basket import addBasket, UserCheckOut


class PostClass:
    def __init__(self):
        pass

    """
        User Checkout     
    """

    @staticmethod
    def exec(posthandler, request, args):
        # Get User basket from token
        try:
            user = checkIfAuth(request)
            UserCheckOut(user['id'])
            return json.dumps({'success': True}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
