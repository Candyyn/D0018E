import datetime

from db.main import Database
import json
import jwt
import bcrypt

# move this secret to somewhere else
secret = "slinky-pursuant-macaw-punk-sandblast-gaming-paralyze"

"""
    Register a new user
"""


def registerUser(email, password, first_name, last_name):
    database = Database().db
    cursor = database.cursor()
    cursor.execute("SELECT user_id, email FROM CUSTOMER WHERE email = '" + email + "'")
    raw = cursor.fetchone()

    if raw is None:
        # User does not exist, create user
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        query = "INSERT INTO CUSTOMER (email, password, salt, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
        values = (email, hashed.decode('utf-8'), salt.decode('utf-8'), first_name, last_name)
        cursor.execute(query, values)
        database.commit()
        return True
    else:
        # User exist
        return False


"""
    Authenticate user
"""


def loginUser(email, password):
    database = Database().db
    cursor = database.cursor()
    query = "SELECT user_id, email, first_name, last_name, role, password FROM CUSTOMER WHERE email = %s"
    values = (email,)
    cursor.execute(query, values)
    raw = cursor.fetchone()
    if raw is not None:
        # User exist, check password
        if bcrypt.checkpw(password.encode('utf-8'), raw[5].encode('utf-8')):
            # Password correct, create token
            token = createToken(
                {"id": raw[0], "email": raw[1], "role": raw[4], "first_name": raw[2], "last_name": raw[3]})
            return token
        else:
            # Password incorrect
            return None


"""
    Create a token
"""


def createToken(user):
    data = {
        "sub": user["email"],
        "name": user["first_name"] + " " + user["last_name"],
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "role": user["role"]
    }

    token = jwt.encode(data, secret, algorithm="HS256")

    # Save token to database
    saveToken(token, data["exp"])

    return token


"""
    Save token to database
"""


def saveToken(token, expires):
    database = Database().db
    cursor = database.cursor()
    # cursor.execute("INSERT INTO TOKENS (tokens, expires) VALUES ('" + token + "', '" + str(expires) + "')")
    database.commit()


"""
    Decode token
"""


def decodeToken(token):
    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
        return data
    except:
        return None


"""
    Verify token
"""


def verifyToken(token):
    data = decodeToken(token)
    if data is None:
        return False
    else:
        # Check if token is expired
        if data["exp"] < datetime.datetime.utcnow():
            return False
        # Check if token is valid
        database = Database().db
        cursor = database.cursor()
        cursor.execute("SELECT user_id, tokens, created, expires FROM TOKENS WHERE tokens = '" + token + "'")
        raw = cursor.fetchone()
        if raw is None:
            return False
        return True
