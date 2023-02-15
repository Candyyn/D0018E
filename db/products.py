import datetime

from db.main import Database
import json
import jwt
import bcrypt

# move this secret to somewhere else
secret = "slinky-pursuant-macaw-punk-sandblast-gaming-paralyze"


def getProducts(page):
    database = Database().db
    cursor = database.cursor()
    query = "SELECT * FROM PRODUCTS LIMIT 10 OFFSET %s"
    values = (page * 10,)
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
            "category": product[5]
        })
    return products


def getProduct(product_id):
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
            "availability": raw[4],
            # "category": raw[5]
        }
    else:
        return None


"""
    Create product
    Permission: 0x01000000
"""


def createProduct(name, description, price, image, availability):
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
    database = Database().db
    cursor = database.cursor()
    query = "DELETE FROM PRODUCTS WHERE prod_id = %s"
    values = (product_id,)
    cursor.execute(query, values)
    database.commit()
    return True
