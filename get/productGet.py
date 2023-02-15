import json

from db.user import getUser


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        from db.products import getProducts
        page = 0
        if len(args) > 0 and args['page'] is not None:
            page = args['page']

        data = getProducts(page)
        return json.dumps({'products': data}, default=str)
