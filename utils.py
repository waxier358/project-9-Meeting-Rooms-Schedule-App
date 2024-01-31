"""
This module defines various constants and namedtuples used for managing room scheduling and user authentication.

Constants:
    ROOMS_LIST (list of tuples): A list containing tuples with room names and their respective IDs.
    TOKEN_EXPIRATION_TIME (int): The time in minutes after which a token expires.

Namedtuples:
    User_salt_and_hash: Represents a user's username, salt, and hashed password.
    Username: Contains user information including ID, username, email address, salt, and hashed password.
    Email_address: Holds user information like ID, username, email address, salt, and hashed password, focusing on email.
    Room: Represents room details including its ID and name.
    Pictures: Stores references to five picture resources.
    Order: Represents an order with details about the orderer and the time interval.
    Token: Contains information about a user token including username, email address, token value, and creation time.

The namedtuples are primarily used to structure data extracted from a database, ensuring consistency and ease of data
handling. The constants provide crucial configuration parameters for the application.
"""
from collections import namedtuple
# a list with tuples(str, int), each tuple contain room's name and id
ROOMS_LIST = [('Classroom', 1), ('Submarine', 2), ('Roofroom', 3)]

# token expiration time express in minutes
TOKEN_EXPIRATION_TIME = 10

# many nametuples use to handle data extracted from database
User_salt_and_hash = namedtuple('user_salt_and_password', 'username salt hash_of_password')

Username = namedtuple('Username', 'id username email_address salt hash_of_password')

Email_address = namedtuple('Email_address', 'id username email_address salt hash_of_password')

Room = namedtuple('Room', 'id room_name room_id')

Pictures = namedtuple('Pictures', 'picture_1 picture_2 picture_3 picture_4 picture_5')

Order = namedtuple('Order', 'order_by order_interval')

Token = namedtuple('Token', 'username, email_address, token, time_of_creation')
