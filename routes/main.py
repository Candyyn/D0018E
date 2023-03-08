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
    },
    "/shop/products": {
        "template": "",
        "get": "productGet.py",
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
    },
    "/verify": {
        "template": "",
        "get": "verifyGet.py",
        "post": "verifyPost.py"
    },
    "/basket/content": {
        "template": "",
        "get": "basketGet.py",
        "delete": "basketDelete.py",
    },
    "/basket/add": {
        "template": "",
        "post": "basketAdd.py",
    },
    "/basket/checkout": {
        "template": "",
        "post": "checkout.py",
    },
    "/review": {
        "template": "",
        "post": "reviewPost.py",
        "get": "reviewGet.py"
    }
}
