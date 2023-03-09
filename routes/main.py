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
    "/product": {
        "template": "",
        "get": "productInfoGet.py",
        "post": "productSendPost.py"
    },
    "/shop/product": {
        "template": "product.html",
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
    },
    "/admin": {
        "template": "admin.html",
    },
    "/admin/users": {
        "template": "",
        "get": "adminUsersGet.py",
        "post": "adminUsersPost.py",
    },
    "/admin/products": {
        "template": "",
        "get": "adminProductsGet.py",
        "post": "adminProductsPost.py",
    },
    "/admin/orders": {
        "template": "",
        "get": "adminOrdersGet.py",
        "post": "adminOrdersPost.py",
    },

}
