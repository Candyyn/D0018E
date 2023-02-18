import datetime

from db.main import Database
import json
import jwt
import bcrypt

# move this secret to somewhere else
secret = "slinky-pursuant-macaw-punk-sandblast-gaming-paralyze"
itemAmount = 10

"""
    Get products
"""


def getProducts(page):
    print("[products.py] getProducts")
    _page = int(page) * itemAmount
    database = Database().db
    cursor = database.cursor()
    query = "SELECT * FROM PRODUCTS LIMIT %s OFFSET %s"
    values = (itemAmount, _page)
    cursor.execute(query, values)
    raw = cursor.fetchall()
    products = []
    for product in raw:
        products.append({
            "product_id": product[0],
            "name": product[1],
            "description": product[2],
            "price": product[3],
            "image": product[4],
            "availability": product[5]
        })
    return products


def getProduct(product_id):
    print("[products.py] getProduct")
    database = Database().db
    cursor = database.cursor()
    query = "SELECT * FROM PRODUCTS WHERE prod_id = %s"
    values = (product_id,)
    cursor.execute(query, values)
    raw = cursor.fetchone()
    if raw is not None:
        return {
            "product_id": raw[0],
            "name": raw[1],
            "description": raw[2],
            "price": raw[3],
            "image": raw[4],
            "availability": raw[5],
            # "category": raw[5]
        }
    else:
        return None


"""
    Create product
    Permission: 0x01000000
"""


def createProduct(name, description, price, image, availability):
    print("[products.py] createProduct")
    database = Database().db
    cursor = database.cursor()
    query = "INSERT INTO PRODUCTS (name, description, price, image, availability) VALUES (%s, %s, %s, %s, %s)"
    values = (name, description, price, image, availability)
    cursor.execute(query, values)
    database.commit()
    return True


"""
    Delete product
    Permission: 0x01000001
"""


def deleteProduct(product_id):
    print("[products.py] deleteProduct")
    database = Database().db
    cursor = database.cursor()
    query = "DELETE FROM PRODUCTS WHERE prod_id = %s"
    values = (product_id,)
    cursor.execute(query, values)
    database.commit()
    return True


def lockProduct(product_id):
    print("[products.py] updateAmount")
    try:
        database = Database().db
        cursor = database.cursor()
        query = "UPDATE PRODUCTS SET availability = availability - 1 WHERE prod_id = %s"
        values = (product_id,)
        cursor.execute(query, values)
        database.commit()
        return True
    except Exception as e:
        return False


def unlockProduct(product_id, amount=1):
    print("[products.py] updateAmount")
    database = Database().db
    cursor = database.cursor()
    query = "UPDATE PRODUCTS SET availability = availability + %s WHERE prod_id = %s"
    values = (amount, product_id)
    cursor.execute(query, values)
    database.commit()
    return True
