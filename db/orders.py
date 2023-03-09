import datetime

from db.main import Database


def getOrders():
    database = Database().db
    cursor = database.cursor()
    cursor.execute("SELECT o.order_id, u.first_name, u.email, p.prod_id 'prod_id', p.name, p.price, oi.quantity "
                   "FROM ORDERS o "
                   "JOIN CUSTOMER u ON o.user_id = u.user_id "
                   "JOIN ORDER_ITEMS oi ON o.order_id = oi.order_id "
                   "JOIN PRODUCTS p ON oi.prod_id = p.prod_id; ")
    raw = cursor.fetchall()
    orders = []
    for order in raw:
        # If order_id is not in orders
        if order[0] not in [o['id'] for o in orders]:
            orders.append({
                "id": order[0],
                "user": {
                    "first_name": order[1],
                    "email": order[2]
                },
                "products": [{
                    "id": order[3],
                    "name": order[4],
                    "price": order[5],
                    "quantity": order[6]
                }]
            })
        else:
            orders[[o['id'] for o in orders].index(order[0])]['products'].append({
                "id": order[3],
                "name": order[4],
                "price": order[5],
                "quantity": order[6]
            })

    return orders


def updateOrder(args):
    database = Database().db
    cursor = database.cursor()
    if args['type'] == 'delete':
        try:
            cursor.execute("START TRANSACTION")
            query = "DELETE FROM ORDER_ITEMS WHERE order_id = %s"
            values = (args["id"],)
            cursor.execute(query, values)
            database.commit()
            return True
        except Exception as e:
            print(e)
            database.rollback()
            return False
        finally:
            cursor.close()
    else:
        try:
            cursor.execute("START TRANSACTION")
            query = "UPDATE ORDERS SET status = %s WHERE order_id = %s"
            values = (args["status"], args["id"])
            cursor.execute(query, values)
            database.commit()
            return True
        except Exception as e:
            print(e)
            database.rollback()
            return False
        finally:
            cursor.close()
