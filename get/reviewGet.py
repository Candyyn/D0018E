import json

from db.user import getUser


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        from db.reviews import getReviews
        prod = 0
        if len(args) > 0 and args['prod'] is not None:
            prod = args['prod']

        data = getReviews(prod)
        return json.dumps({'reviews': data}, default=str)
