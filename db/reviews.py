from db.main import Database


def addReview(user, product_id, comment, rating):
    database = Database().db
    cursor = database.cursor()

    _rating = int(rating)

    if 0 >= _rating < 6:
        return False

    query = "START TRANSACTION;"
    query += "INSERT INTO REVIEWS (user_id, prod_id, comment, rating) VALUES (%s, %s, %s, %s);"
    query += "COMMIT;"
    values = (user['id'], product_id, comment, _rating)
    cursor.execute(query, values)
    database.commit()
    return True


def getRating(product_id):
    database = Database().db
    cursor = database.cursor()
    query = "SELECT FORMAT(AVG(rating), 0) 'Rating' FROM `REVIEWS` WHERE prod_id = %s"
    values = (product_id,)
    cursor.execute(query, values)
    raw = cursor.fetchone()
    if raw:
        return {"rating": raw[0]['Rating']}
    else:
        return {"rating": 0}


def getReviews(product_id):
    database = Database().db
    cursor = database.cursor()
    # query = "SELECT * FROM `REVIEWS` WHERE prod_id = %s"
    query = """SELECT REVIEWS.*, CUSTOMER.first_name, CUSTOMER.last_name 
                FROM REVIEWS 
                JOIN CUSTOMER ON REVIEWS.user_id = CUSTOMER.user_id;
                """
    values = (product_id,)
    cursor.execute(query, values)
    raw = cursor.fetchall()

    reviews = []
    for review in raw:
        reviews.append({
            "user_id": review[0],
            "prod_id": review[1],
            "comment": review[2],
            "rating": review[3],
            "date": review[4],
            "first_name": review[5],
            "last_name": review[6]
        })
    return reviews
