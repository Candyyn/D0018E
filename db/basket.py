from db.main import Database
from db.products import getProduct, lockProduct, unlockProduct

"""
    Get basket
    TODO: CHANGE order_id to user_id so we link it correctly.    
"""


def getBasket(user_id):
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

    # get product
    product = getProduct(product_id)
    product_available = product["availability"]
    product_price = product["price"]

    # Check if product is available
    if product_available < 1:
        return False

    # Acquire a lock on the product before adding it to the basket
    if not lockProduct(product_id):
        return False

    try:
        # Start a transaction
        database = Database().db
        cursor = database.cursor()
        cursor.execute("START TRANSACTION;")

        # Add product to basket
        query = "INSERT INTO SHOPPING_CART (user_id, product_id, amount) VALUES (%s, %s, %s) " \
                "ON DUPLICATE KEY UPDATE amount = amount + VALUES(amount)"
        values = (user_id, product_id, 1)
        cursor.execute(query, values)

        # Commit the transaction
        database.commit()
        return True

    except Exception as e:
        # Rollback the transaction in case of an error
        database.rollback()
        return False
    finally:
        cursor.close()


def deleteFromBasket(user_id, cart_id, amount):
    # If Amount is 0, delete entire row else update amount
    try:
        database = Database().db
        cursor = database.cursor()
        cursor.execute("START TRANSACTION;")

        if int(amount) == 0:

            # Get product_id and amount

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
        database.rollback()
        return False
    finally:
        cursor.close()


def UserCheckOut(user_id):
    # Delete row from SHOPPING_CART
    database = Database().db
    cursor = database.cursor()
    try:
        cursor.execute("START TRANSACTION;")
        # query = "DELETE FROM SHOPPING_CART WHERE user_id = %s;"

        select_query = '''
        SELECT user_id, product_id, amount, 0 
        FROM SHOPPING_CART
        WHERE user_id = %s
        '''

        cursor.execute(select_query, (user_id,))
        rows = cursor.fetchall()

        order_items = []
        total_price = 0

        for row in rows:
            product_id, amount, price = row[1:]
            order_items.append((product_id, amount, price))
            total_price += amount * price

        insert_order_query = '''
        INSERT INTO ORDERS (user_id, total_price, status)
        VALUES (%s, %s, %s)
        '''

        insert_order_item_query = '''
        INSERT INTO ORDER_ITEMS (order_id, prod_id, quantity, price)
        VALUES (%s, %s, %s, %s)
        '''

        cursor.execute(insert_order_query, (user_id, total_price, 0))
        order_id = cursor.lastrowid

        for item in order_items:
            product_id, amount, price = item
            cursor.execute(insert_order_item_query, (order_id, product_id, amount, price))

        database.commit()
        return True
    except Exception as e:
        print(e)
        database.rollback()
        return False
    finally:
        cursor.close()


"""
Add a product
"""


def addProduct(name, description, price, image, availability):
    # Insert product into PRODUCTS
    database = Database().db
    cursor = database.cursor()
    query = "START TRANSACTION;"
    query += "INSERT INTO PRODUCTS (name, description, price, image, availability) VALUES (%s, %s, %s, %s, %s)"
    query += "COMMIT;"
    values = (name, description, price, image, availability)
    cursor.execute(query, values)
    database.commit()
    return True


"""
Delete Product
"""


def removeProduct(product_id):
    # Delete row from PRODUCTS
    database = Database().db
    cursor = database.cursor()
    query = "START TRANSACTION;"
    query = "DELETE FROM PRODUCTS WHERE prod_id = %s;"
    query += "COMMIT;"
    values = (product_id,)
    cursor.execute(query, values)
    database.commit()
    return True
