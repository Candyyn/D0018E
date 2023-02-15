routes = {
    "/": {
        "template": "index.html",
        "post": "indexPost.py"
    },
    "/index": {
        "template": "index.html",
        "post": "indexPost.py",
    },
    "/shop": {
        "template": "Shop.html",
        "post": "indexPost.py"
    },
    "/login": {
        "template": "login.html",
        "post": "loginPost.py"
    },
    "/register": {
        "template": "register.html",
        "post": "registerPost.py"
    },
    "/checkout": {
        "template": "checkout.html",
        "post": "indexPost.py"
    },
    "/verify": {
        "template": "",
        "get": "verifyGet.py",
        "post": "verifyPost.py"
    },
    "/test": {
        "template": "",
        "get": "testGet.py",
    },
}
