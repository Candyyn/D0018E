import json

from db.user import getUser, checkIfAuth
from db.reviews import addReview


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
            product_id = args['product_id']

            comment = args['comment']
            rate = args['rate']

            success = addReview(user, product_id, comment, rate)

            return json.dumps({'success': str(success)}, default=str)
        except Exception as e:
            return json.dumps({'error': e}, default=str)
