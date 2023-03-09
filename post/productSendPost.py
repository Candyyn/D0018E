import json

from db.user import getUser, checkIfAuth, hasPermission, updateUser
from db.products import createComment


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
            if len(args) == 0:
                raise Exception('No id given')
            return json.dumps({'success': createComment(user, args)}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
