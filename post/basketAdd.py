import json

from db.user import getUser, checkIfAuth
from db.basket import addBasket


class PostClass:
    def __init__(self):
        pass

    """
        Add product to basket
        
    
    """

    @staticmethod
    def exec(posthandler, request, args):
        # Get User basket from token
        try:
            if len(args) == 0:
                raise Exception('No product id given')
            user = checkIfAuth(request)
            product_id = args['product_id']
            response = addBasket(user['id'], product_id)
            return json.dumps({'success': str(response)}, default=str)
        except Exception as e:
            print(e)
            return json.dumps({'error': e}, default=str)
