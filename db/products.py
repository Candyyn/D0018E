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
    query = """SELECT p.*, FORMAT(IFNULL(AVG(r.rating), 0), 0) AS avg_rating
                FROM PRODUCTS p
                LEFT JOIN REVIEWS r ON p.prod_id = r.prod_id
                GROUP BY p.prod_id
                LIMIT %s OFFSET %s;"""
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
            "availability": product[5],
            "rating": int(product[6])
        })
    return products


def getProduct(product_id):
    print("[products.py] getProduct")
    database = Database().db
    cursor = database.cursor()
    #query = "SELECT * FROM PRODUCTS WHERE prod_id = %s"
    query = """SELECT p.*, IFNULL(AVG(r.rating), 0) AS avg_rating
                    FROM PRODUCTS p
                    LEFT JOIN REVIEWS r ON p.prod_id = r.prod_id
                    WHERE p.prod_id = %s
                    GROUP BY p.prod_id;
                    """
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
            "rating": raw[6]
        }
    else:
        return None


"""
    Create product
    Permission: 0x01000000
"""


def createProduct(name, description, price, image, availability):
    print("[products.py] createProduct")
    try:
        database = Database().db
        cursor = database.cursor()
        # Begin transaction
        cursor.execute("START TRANSACTION")

        query = "INSERT INTO PRODUCTS (name, description, price, image, availability) VALUES (%s, %s, %s, %s, %s)"
        values = (name, description, price, image, availability)
        cursor.execute(query, values)

        # Commit transaction if there are no errors
        database.commit()
        return True
    except:
        # Rollback transaction if there are errors
        database.rollback()
        return False
    finally:
        cursor.close()


"""
    Delete product
    Permission: 0x01000001
"""


def deleteProduct(product_id):
    print("[products.py] deleteProduct")
    database = Database().db
    try:
        cursor = database.cursor()
        # Begin transaction
        cursor.execute("START TRANSACTION")

        query = "DELETE FROM PRODUCTS WHERE prod_id = %s"
        values = (product_id,)
        cursor.execute(query, values)

        # Commit transaction if there are no errors
        database.commit()
        return True
    except:
        # Rollback transaction if there are errors
        database.rollback()
        return False
    finally:
        cursor.close()


def lockProduct(product_id):
    print("[products.py] updateAmount")
    try:
        database = Database().db
        cursor = database.cursor()
        # Start transaction
        cursor.execute("START TRANSACTION")
        query = "UPDATE PRODUCTS SET availability = availability - 1 WHERE prod_id = %s"
        values = (product_id,)
        cursor.execute(query, values)
        # Commit transaction if no errors
        database.commit()
        return True
    except Exception as e:
        # Rollback transaction if there are errors
        database.rollback()
        return False
    finally:
        cursor.close()


def unlockProduct(product_id, amount=1):
    print("[products.py] updateAmount")
    try:
        database = Database().db
        cursor = database.cursor()
        # Begin transaction
        cursor.execute("START TRANSACTION")

        query = "UPDATE PRODUCTS SET availability = availability + %s WHERE prod_id = %s"
        values = (amount, product_id)
        cursor.execute(query, values)

        # Commit transaction if there are no errors
        database.commit()
        return True
    except:
        # Rollback transaction if there are errors
        database.rollback()
        return False
    finally:
        cursor.close()
