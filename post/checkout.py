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
            # TODO: Right now it just deletes the basket. We need to implement a checkout function
            UserCheckOut(user['id'])
            print('TODO: Implement correct checkout')
            return json.dumps({'success': True}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
