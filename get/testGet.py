from db.user import getUser


class GetClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        return "Hello"
