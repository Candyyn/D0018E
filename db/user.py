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


def registerUser(email, password, first_name, last_name, phone, address):
    database = Database().db
    cursor = database.cursor()
    cursor.execute("SELECT user_id, email FROM CUSTOMER WHERE email = '" + email + "'")
    raw = cursor.fetchone()

    if raw is None:
        # User does not exist, create user
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        query = "INSERT INTO CUSTOMER (email, password, salt, first_name, last_name, phone, address) VALUES (%s, %s, " \
                "%s, %s, %s, %s, %s)"
        values = (email, hashed.decode('utf-8'), salt.decode('utf-8'), first_name, last_name, phone, address)
        cursor.execute(query, values)
        database.commit()
        # get row
        query = "SELECT CUSTOMER.user_id, CUSTOMER.email, CUSTOMER.first_name, " \
                "CUSTOMER.last_name, CUSTOMER.password, ROLES.role_id, ROLES.name, ROLES.bitwise FROM CUSTOMER " \
                "INNER JOIN ROLES ON CUSTOMER.role = ROLES.role_id WHERE email = %s"
        values = (email,)
        cursor.execute(query, values)
        raw = cursor.fetchone()

        return createUserResponse(raw)
    else:
        # User exist
        return False


"""
    Authenticate user
"""


def loginUser(email, password):
    database = Database().db
    cursor = database.cursor()
    # Select CUSTOMER from email, and get role from ROLES based on role
    query = "SELECT CUSTOMER.user_id, CUSTOMER.email, CUSTOMER.first_name, " \
            "CUSTOMER.last_name, CUSTOMER.password, ROLES.role_id, ROLES.name, ROLES.bitwise FROM CUSTOMER " \
            "INNER JOIN ROLES ON CUSTOMER.role = ROLES.role_id WHERE email = %s"
    values = (email,)
    cursor.execute(query, values)
    raw = cursor.fetchone()
    if raw is not None:
        # User exist, check password
        if bcrypt.checkpw(password.encode('utf-8'), raw[4].encode('utf-8')):
            # Password correct, create token
            return createUserResponse(raw)
        else:
            # Password incorrect
            return None


"""
    Create user data     
"""


def createUserResponse(userRaw):
    token = createToken(
        {"id": userRaw[0], "email": userRaw[1], "role": {"id": userRaw[5], "name": userRaw[6], "bit": bin(userRaw[7])},
         "first_name": userRaw[2], "last_name": userRaw[3]})

    data = {
        "id": userRaw[0],
        "email": userRaw[1],
        "first_name": userRaw[2],
        "last_name": userRaw[3],
        "role": {
            "id": userRaw[5],
            "name": userRaw[6],
            "bit": bin(userRaw[7])
        }
    }

    return data, token


def getUser(token):
    data = decodeToken(token)
    if data is None:
        return None
    else:
        return {
            "id": data["sub"],
            "email": data["email"],
            "first_name": data["name"].split(" ")[0],
            "last_name": data["name"].split(" ")[1],
            "role": data["role"]
        }


"""
    Create a token
"""


def createToken(user):
    data = {
        "sub": user["id"],
        "email": user["email"],
        "name": user["first_name"] + " " + user["last_name"],
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "role": user["role"]
    }

    token = jwt.encode(data, secret, algorithm="HS256")

    # Save token to database
    saveToken(user, token, data["exp"])

    return token


"""
    Save token to database
"""


def saveToken(user, token, expires):
    database = Database().db
    cursor = database.cursor()
    query = "INSERT INTO TOKENS (user_id, tokens, expires) VALUES (%s, %s, %s) " \
            "ON DUPLICATE KEY UPDATE tokens = VALUES(tokens), expires = VALUES(expires)"
    values = (user['id'], token, expires)

    cursor.execute(query, values)
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
        then = data["exp"]
        now = datetime.datetime.utcnow() + datetime.timedelta(days=0)
        if then < int(now.timestamp()):
            return False
        # Check if token is valid
        database = Database().db
        cursor = database.cursor()
        cursor.execute("SELECT user_id, tokens, created, expires FROM TOKENS WHERE tokens = '" + token + "'")
        raw = cursor.fetchone()
        if raw is None:
            return False
        return True


"""
    Check if user has permission
"""


def hasPermission(required, userperm):
    # This is a bitwise permission check
    # If the user has the required permission, the bitwise AND will return the same value as the required permission
    # If the user does not have the required permission, the bitwise AND will return 0
    if required & userperm == required:
        return True
    else:
        return False


def checkIfAuth(request):
    token = request.headers.get("Authorization")
    if token is None:
        raise Exception("No token provided")
    else:

        # Remove Bearer from token
        token = token.replace("Bearer ", "")

        if verifyToken(token):
            return getUser(token)
        else:
            raise Exception("Invalid token")
