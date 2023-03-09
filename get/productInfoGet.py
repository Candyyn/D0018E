import json

from db.user import getUser


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        from db.products import getProduct
        id = -1
        if len(args) > 0 and args['id'] is not None:
            id = args['id']

        print(id)
        data = getProduct(id)
        return json.dumps({'product': data}, default=str)
