from db.main import Database
from db.products import getProduct

"""
    Get basket
    TODO: CHANGE order_id to user_id so we link it correctly.    
"""


def getBasket(user_id):
    print('[basket.py] getBasket(user_id) user_id: ' + str(user_id))
    # Get user basket from SHOPPING_CART
    database = Database().db
    cursor = database.cursor()

    # Get user basket from SHOPPING_CART and join in product_id from PRODUCTS
    query = "SELECT SHOPPING_CART.cart_id, SHOPPING_CART.product_id, SHOPPING_CART.price, " \
            "PRODUCTS.prod_id, PRODUCTS.name, PRODUCTS.description, PRODUCTS.image, PRODUCTS.price FROM " \
            "SHOPPING_CART INNER JOIN PRODUCTS ON SHOPPING_CART.product_id = PRODUCTS.prod_id WHERE order_id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    raw = cursor.fetchall()
    basket = []
    for item in raw:
        basket.append({
            "cart_id": item[0],
            "product_id": item[1],
            "amount": item[2],
            "price": item[3],
            "name": item[4],
            "description": item[5],
            "image": item[6],
            "price": item[7]
        })
    return basket


"""
    Add product to basket
"""


def addBasket(user_id, product_id):
    print('[basket.py] addBasket(user_id, product_id) user_id: ' + str(user_id) + ' product_id: ' + str(product_id))
    # get product
    product = getProduct(product_id)
    product_price = product["price"]

    # Add product to basket
    database = Database().db
    cursor = database.cursor()
    query = "INSERT INTO SHOPPING_CART (product_id, amount, price) VALUES (%s, %s, %s)"
    values = (product_id, 1, product_price)
    cursor.execute(query, values)
    database.commit()
    return True
