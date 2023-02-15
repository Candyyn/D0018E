from db.user import getUser


class PostClass:
    def __init__(self):
        pass

    @staticmethod
    def exec(posthandler, request, args):
        print("hello")
        return "Hello"
