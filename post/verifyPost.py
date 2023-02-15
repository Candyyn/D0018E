from db.user import getUser


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        return getUser(request.headers['authorization'])
