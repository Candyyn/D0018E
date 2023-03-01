import json

from db.user import getUser, checkIfAuth, hasPermission
from db.basket import addProduct


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
                if len(posthandler.data_string) == 0:
                    posthandler.setStatus(400)
                    posthandler.contentType = 'text/json'
                    return json.dumps({'error': "Invalid Arguments"})
                else:
                    args = posthandler.data_string
            user = checkIfAuth(request)
            hasPermission(user, 0x01000000)
            addProduct(args);
            return json.dumps({'success': True}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
