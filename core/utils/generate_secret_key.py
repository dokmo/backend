from datetime import datetime, timedelta

import bcrypt
from jose import jwt

SECRET_KEY = "cd78291935e8759bba3cc81eb0c24be4940baf1ec4df926fdf32d3bf7a548b34"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """
    Creates a JWT access token with a salt and expiration.
    :param data: Payload data to include in the token.
    :param password: A unique random string to add to the payload.
    :return: Encoded JWT token as a string.
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decodes a JWT access token and returns the payload.
    :param token: The JWT token to decode.
    :return: Decoded payload data.
    """
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except Exception as e:
        print("Token verification failed:", e)
        return None


# Example usage
# Step 1: Create random salt
user_info = {'user_id': 9318597893}
token = create_access_token(data = user_info)
bytes_hashed_password = bcrypt.hashpw(user_info, bcrypt.gensalt())

print("bytes_hashed_password:", bytes_hashed_password)

# Step 2: Create a token with payload and bytes_password
payload = {"sub": "user@example.com"}
token = create_access_token(data = payload, password = str(bytes_hashed_password))
print("\nEncoded JWT Token:\n", token)

# Step 3: Decode the token to verify the payload and salt
decoded_payload = decode_access_token(token)
print("\nDecoded Payload:\n", decoded_payload)
