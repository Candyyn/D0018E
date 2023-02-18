import json

from db.basket import getBasket, deleteFromBasket
from db.user import getUser, checkIfAuth


class DeleteClass:
    def __init__(self):
        pass

    """
        Delete Item In Basket
        Args: cart_id, (all or 1)
    """

    @staticmethod
    def exec(deletehandler, request, args):
        # Get User basket from token
        # _user = getUser(request.headers['authorization'])

        if len(args) == 0:
            if len(deletehandler.data_string) == 0:
                deletehandler.setStatus(400)
                deletehandler.contentType = 'text/json'
                return json.dumps({'error': "Invalid Arguments"})
            else:
                args = deletehandler.data_string

        try:
            user = checkIfAuth(request)
            basket = deleteFromBasket(user['id'], args['cart_id'], args['amount'])
            return json.dumps({'status': basket}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
