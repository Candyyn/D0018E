from db.main import Database
from db.products import getProduct, lockProduct, unlockProduct

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
    query = "SELECT SHOPPING_CART.cart_id, SHOPPING_CART.product_id," \
            "SHOPPING_CART.amount, PRODUCTS.name, PRODUCTS.description, PRODUCTS.image, PRODUCTS.price FROM " \
            "SHOPPING_CART INNER JOIN PRODUCTS ON SHOPPING_CART.product_id = PRODUCTS.prod_id WHERE user_id = %s " \
            "AND amount > 0"
    values = (user_id,)
    cursor.execute(query, values)
    raw = cursor.fetchall()
    basket = []
    for item in raw:
        basket.append({
            "cart_id": item[0],
            "product_id": item[1],
            "amount": item[2],
            "name": item[3],
            "description": item[4],
            "image": item[5],
            "price": item[6],
        })
    return basket


"""
    Add product to basket
"""


def addBasket(user_id, product_id):
    print('[basket.py] addBasket(user_id, product_id) user_id: ' + str(user_id) + ' product_id: ' + str(product_id))
    # get product
    product = getProduct(product_id)
    product_available = product["availability"]
    product_price = product["price"]


    # Check if product is available
    if product_available < 1:
        return False

    if lockProduct(product_id) is False:
        return False

    # Add product to basket
    database = Database().db
    cursor = database.cursor()
    query = "INSERT INTO SHOPPING_CART (user_id, product_id, amount) VALUES (%s, %s, %s) " \
            "ON DUPLICATE KEY UPDATE amount = amount + VALUES(amount)"
    values = (user_id, product_id, 1)
    cursor.execute(query, values)
    database.commit()
    return True


def deleteFromBasket(user_id, cart_id, amount):
    # If Amount is 0, delete entire row else update amount
    try:
        if int(amount) == 0:

            # Get product_id and amount
            database = Database().db
            cursor = database.cursor()
            query = "SELECT amount, product_id FROM SHOPPING_CART WHERE cart_id = %s AND user_id = %s;"
            values = (cart_id, user_id)
            cursor.execute(query, values)
            raw = cursor.fetchone()
            amount = raw[0]
            prod_id = raw[1]

            # Unlock product
            unlockProduct(prod_id, amount)

            # Then delete row
            query = "DELETE FROM SHOPPING_CART WHERE cart_id = %s AND user_id = %s;"
            values = (cart_id, user_id)
            cursor.execute(query, values)
            database.commit()
            return True
        else:
            # Get product_id
            database = Database().db
            cursor = database.cursor()
            query = "SELECT product_id FROM SHOPPING_CART WHERE cart_id = %s AND user_id = %s;"
            values = (cart_id, user_id)
            cursor.execute(query, values)
            raw = cursor.fetchone()
            prod_id = raw[0]

            # Unlock product
            unlockProduct(prod_id)
            query = "UPDATE SHOPPING_CART SET amount = amount - 1 WHERE cart_id = %s AND user_id = %s AND amount > 0"
            values = (cart_id, user_id)
            cursor.execute(query, values)
            database.commit()
            return True
    except Exception as e:
        print(e)
        return False


def UserCheckOut(user_id):
    # Delete row from SHOPPING_CART
    database = Database().db
    cursor = database.cursor()
    query = "DELETE FROM SHOPPING_CART WHERE user_id = %s;"
    values = (user_id,)
    cursor.execute(query, values)
    database.commit()
    return True
