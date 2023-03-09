import json

from db.user import getUser, checkIfAuth, hasPermission, updateUser


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
            user = checkIfAuth(request)
            # TODO: Update the permission to the correct one
            hasPermission(user, 0x01000100)
            if len(args) == 0:
                raise Exception('No id given')
            return json.dumps({'success': updateOrders(args)}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
