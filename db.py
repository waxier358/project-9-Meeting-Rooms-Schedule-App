import sqlite3
import bcrypt
from utils import User_salt_and_hash, Username, Email_address, ROOMS_LIST, Room, Pictures, Order
from uuid import uuid4
import os

from utils import Token


class Database:
    """This class creates and controls database."""
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.database_exist = self.check_if_database_exist()
        self.open()

    @staticmethod
    def check_if_database_exist() -> bool:
        """Check if database exists in 'database' folder
           Returns:
                bool: True if database exists, False otherwise
        """

        path = 'database'
        if len(os.listdir(path=path)) == 0:
            return False
        return True

    @staticmethod
    def create_salt_and_hash_of_password(password: str) -> dict:
        """Create salt and hash for a password based on the input string
           Args:
                password(str): The string based on which the hash will be generated.
           Returns:
                dict: A dictionary containing the salt and hashed password.
        """
        salt = bcrypt.gensalt()
        hash_of_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        return {'salt': salt,
                'hash_of_password': hash_of_password}

    @staticmethod
    def convert_to_binary(folder_name: str, filename: str) -> bytes:
        """Convert an image to a binary file format.
           Args:
                folder_name(str): The name of the folder where the image is located.
                filename(str): The name of the file to be converted.
           Returns:
                bytes: The content of 'filename.png' in binary format.
        """
        with open(f'images/{folder_name}/{filename}', 'rb') as file:
            return file.read()

    @staticmethod
    def write_to_file(folder_name: str, filename: str, data: bytes):
        """Creates a binary file in the specified folder with the provided data.
           Args:
           folder_name (str): The name of the folder where the file will be created.
           filename (str): The name of the file to be created.
           data: The data to be written to the file.
        """
        with open(f'images/{folder_name}/{filename}', 'wb') as file:
            file.write(data)

    def create_table(self):
        """This method creates tables in database."""
        ddl = """CREATE TABLE IF NOT EXISTS users 
                 (  
                    id                INTEGER PRIMARY KEY,
                    username          TEXT UNIQUE NOT NULL,
                    email_address     TEXT UNIQUE NOT NULL,
                    salt              TEXT NOT NULL,
                    hash_of_password  TEXT NOT NULL
                 );
                 CREATE TABLE IF NOT EXISTS rooms 
                 (
                    id          INTEGER PRIMARY KEY,
                    room_name   TEXT UNIQUE NOT NULL,
                    room_id     INTEGER UNIQUE NOT NULL
                 );
                 CREATE TABLE IF NOT EXISTS pictures 
                 (
                    id          INTEGER PRIMARY KEY,
                    room_id     INTEGER UNIQUE NOT NULL,
                    room_name   TEXT UNIQUE NOT NULL,
                    picture_1   BLOB NOT NULL,
                    picture_2   BLOB NOT NULL,
                    picture_3   BLOB NOT NULL,
                    picture_4   BLOB NOT NULL,
                    picture_5   BLOB NOT NULL,
                    FOREIGN KEY (room_id) REFERENCES rooms (room_id),
                    FOREIGN KEY (room_name) REFERENCES rooms (room_name)
                 );
                 CREATE TABLE IF NOT EXISTS schedule
                 (
                    id              INTEGER PRIMARY KEY,
                    room_name       TEXT NOT NULL,
                    order_by        TEXT NOT NULL,
                    order_date      TEXT NOT NULL,
                    order_interval  TEXT NOT NULL,
                    FOREIGN KEY (room_name) REFERENCES rooms (room_name),
                    FOREIGN KEY (order_by)  REFERENCES users (username) 
                 );
                 CREATE TABLE IF NOT EXISTS tokens 
                 (  
                    id                INTEGER PRIMARY KEY,
                    username          TEXT UNIQUE NOT NULL,
                    email_address     TEXT UNIQUE NOT NULL,
                    token             TEXT NOT NULL,
                    time_of_creation  DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES users (username),
                    FOREIGN KEY (email_address) REFERENCES users (email_address)
                 );
        """
        self.conn.executescript(ddl)

    def add_new_user_to_db(self, username: str, email_address: str, password: str):
        """Creates a salt and hash based on the provided password and adds the username,
           email address, salt, and hash to the database.
           Args:
           username (str): The username to be added to the database.
           email_address (str): The email address associated with the username.
           password (str): The password for which the salt and hash are to be created.
        """
        salt_and_hash_of_password = self.create_salt_and_hash_of_password(password)
        self.conn.execute('INSERT INTO users(username, email_address, salt, hash_of_password) VALUES(?,?,?,?);',
                          (username, email_address, salt_and_hash_of_password.get('salt'),
                           salt_and_hash_of_password.get('hash_of_password')))
        self.conn.commit()

    def update_password(self, username: str, email_address: str, password: str):
        """Creates a salt and hash based on the provided password string and updates the
           user's salt and hash in the database using the given username and email address.
           Args:
           username (str): The username of the user whose salt and hash need to be updated.
           email_address (str): The email address of the user to match in the database.
           password (str): The password from which the new salt and hash will be generated.
        """
        salt_and_hash_of_password = self.create_salt_and_hash_of_password(password)
        query = """UPDATE users
                    SET 
                        salt=?,
                        hash_of_password=?
                    WHERE
                        username=? AND email_address=?"""
        data = (salt_and_hash_of_password.get('salt'), salt_and_hash_of_password.get('hash_of_password'), username,
                email_address)
        self.conn.execute(query, data)
        self.conn.commit()

    def get_user_by_username(self, username: str) -> Username:
        """Retrieves a record from the database for a specified username.
           Args:
           username (str): The username for which the record is to be retrieved.
           Returns:
           Username: A namedtuple 'Username', containing fields 'id', 'username',
           'email_address', 'salt', and 'hash_of_password'.
        """
        fetch = self.conn.execute(f'SELECT * FROM users WHERE username=?;', (username,)).fetchone()
        if fetch:
            return Username(*fetch)

    def get_user_by_email(self, email_address: str) -> Email_address:
        """Retrieves a record from the database for a specified email address.
           Args:
           email_address (str): The email address for which the record is to be retrieved.
           Returns:
           Email_address: A namedtuple 'Email_address', containing fields 'id', 'username',
           'email_address', 'salt', and 'hash_of_password'.
        """
        fetch = self.conn.execute(f'SELECT * FROM users WHERE email_address=?;', (email_address,)).fetchone()
        if fetch:
            return Email_address(*fetch)

    def get_salt_and_password_by_username_email(self, username: str) -> User_salt_and_hash:
        """Retrieves the salt and hash of the password from the database for a specified username.
           Args:
           username (str): The username for which the salt and hash are to be retrieved.
           Returns:
           User_salt_and_hash: A namedtuple 'User_salt_and_hash', containing fields
                        'username', 'salt', and 'hash_of_password'.
        """
        fetch = self.conn.execute('SELECT username, salt, hash_of_password FROM users WHERE username=?;',
                                  (username,)).fetchone()
        if fetch:
            return User_salt_and_hash(*fetch)

    def add_all_rooms_to_db(self):
        """Adds rooms from ROOMS_LIST to the database."""
        query = 'INSERT INTO rooms(room_name, room_id) VALUES(?,?);'
        self.conn.executemany(query, ROOMS_LIST)
        self.conn.commit()

    def insert_new_schedule_in_db(self, room_name: str, order_by: str, order_date: str, order_interval: str):
        """Creates a new schedule record in the database.
           Args:
           room_name (str): The name of the room for which the schedule is being created.
           order_by (str): The name of the user who made the schedule.
           order_date (str): The date of the schedule.
           order_interval (str): The interval of the schedule.
        """
        new_schedule_tuple = (room_name, order_by, order_date, order_interval)
        query = 'INSERT INTO schedule(room_name, order_by, order_date, order_interval) VALUES(?,?,?,?);'
        self.conn.execute(query, new_schedule_tuple)
        self.conn.commit()

    def add_pictures_to_db(self, room_name: str, room_id: int):
        """Reads pictures from a specified folder and adds them to the picture table in the database.
           Each room is represented by 5 images. Each record in the pictures table will contain the room_name,
           room_id, and all 5 pictures.
           Args:
           room_name (str): The name of the folder where pictures are stored and also the prefix for each picture
                     name (all pictures are in .png format).
           room_id (int): An integer number associated with each room.
        """
        pictures_1 = self.convert_to_binary(f"{room_name}", f"{room_name}1.png")
        pictures_2 = self.convert_to_binary(f"{room_name}", f"{room_name}2.png")
        pictures_3 = self.convert_to_binary(f"{room_name}", f"{room_name}3.png")
        pictures_4 = self.convert_to_binary(f"{room_name}", f"{room_name}4.png")
        pictures_5 = self.convert_to_binary(f"{room_name}", f"{room_name}5.png")

        room_name_tuple = (room_name.title(), room_id, pictures_1, pictures_2, pictures_3, pictures_4, pictures_5)

        query = ('INSERT INTO pictures(room_name, room_id, picture_1, picture_2, picture_3, picture_4, picture_5)'
                 ' VALUES(?,?,?,?,?,?,?);')
        self.conn.execute(query, room_name_tuple)
        self.conn.commit()

    def get_pictures_from_room_with_name(self, room_name: str) -> Pictures:
        """Retrieves all pictures associated with a room identified by the given room_name.
           Args:
           room_name (str): The name of the room for which pictures are to be retrieved.
           Returns:
           Pictures: A namedtuple 'Pictures', containing fields 'picture_1', 'picture_2', 'picture_3', 'picture_4'
           and 'picture_5' representing the associated pictures.
        """
        fetch = self.conn.execute('SELECT picture_1, picture_2, picture_3, picture_4, picture_5 FROM pictures WHERE'
                                  ' room_name=?;',
                                  (room_name,)).fetchone()
        if fetch:
            return Pictures(*fetch)

    def get_all_rooms_form_db(self) -> list:
        """Retrieves the names of all rooms from the pictures table.
           Returns:
           list of Room: A list of namedtuples 'Room', each containing fields 'id', 'room_name' and 'room_id'.
        """
        query = 'SELECT  * FROM rooms'
        fetch = self.conn.execute(query).fetchall()

        if fetch:
            return [Room(*room) for room in fetch]

    def get_schedule_for_current_date_and_room(self, room_name: str, current_date: str) -> list:
        """Retrieves all schedules from the schedule table associated with a given room_name and current_date.
           Args:
           room_name (str): The name of the room for which schedules are to be retrieved.
           current_date (str): The specific date for which schedules are being queried.
           Returns:
           list of Order: A list of namedtuples 'Order', each containing fields 'order_by' and 'order_interval',
           representing the user who made the schedule and the schedule interval.
        """
        fetch = self.conn.execute('SELECT order_by, order_interval FROM schedule WHERE room_name=? AND order_date=?;',
                                  (room_name, current_date)).fetchall()
        if fetch:
            return [Order(*order) for order in fetch]

    def delete_token_by_username_and_email_address(self, username: str, email_address: str):
        """Deletes the token associated with a specific username and email address from the tokens table.
           Args:
           username (str): The username associated with the token.
           email_address (str): The email address associated with the token.
        """
        query = "DELETE FROM tokens WHERE username = ? AND email_address = ?"
        self.conn.execute(query, (username, email_address))
        self.conn.commit()

    def create_new_token(self, username: str, email_address: str):
        """Creates a new token associated with a username and email address, and inserts it into the tokens table.
           The tokens table includes fields for username, email_address, token and time_of_creation. The username and
           email_address are provided as arguments. The token is generated within this method, and the time_of_creation
           is set to the current time by default.
           Args:
           username (str): The username with which the new token will be associated.
           email_address (str): The email address with which the new token will be associated.
        """
        token = str(uuid4())

        new_token_tuple = (username, email_address, token)

        query = 'INSERT INTO tokens(username, email_address, token) VALUES(?,?,?);'
        self.conn.execute(query, new_token_tuple)
        self.conn.commit()

    def get_token_from_db(self, username: str, email_address: str) -> Token:
        """Retrieves a record from the tokens table associated with the specified username and email address.
           Args:
           username (str): The username associated with the token record.
           email_address (str): The email address associated with the token record.
           Returns:
           Token: A namedtuple 'Token', containing fields 'username', 'email_address', 'token' and 'time_of_creation',
           representing the retrieved token record.
        """
        fetch = self.conn.execute('SELECT username, email_address, token, time_of_creation FROM tokens'
                                  ' WHERE username=? AND email_address=?;',
                                  (username, email_address)).fetchone()
        if fetch:
            return Token(*fetch)

    def open(self):
        """Establishes a connection with the 'mrs' database. If the database does not exist, this method creates the
           database and all required tables within it."""
        self.conn = sqlite3.connect('database/mrs.db')
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.conn.commit()
        if not self.database_exist:
            self.create_table()
            self.add_all_rooms_to_db()
            self.add_pictures_to_db("classroom", 1)
            self.add_pictures_to_db("submarine", 2)
            self.add_pictures_to_db("roofroom", 3)

    def close(self):
        """Closes the cursor and the connection to the current database."""
        self.cursor.close()
        self.conn.close()


class Node:
    """Creates a node for use in a Circular Double Linked List (CDLL).
       This node is designed to be a part of a CDLL, containing the necessary properties for such a structure. Each node
       has a 'data' attribute to store its value and two pointer attributes, 'next' and 'prev', to point to the next and
       previous nodes in the list, respectively. In a CDLL, these pointers allow for bidirectional traversal and ensure
       that the list is circular, with the last node linking back to the first node, and vice versa."""
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class CircularDoubleLinkedList:
    """Creates a circular double linked list.
       This implementation of a circular double linked list allows for bidirectional traversal. Each node in the list
       contains two links: one to the next node and one to the previous node. The list is circular, meaning the last
       node's 'next' link points back to the first node, and the first node's 'previous' link points back to the last
       node."""
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_value = None

    def add_new_value(self, new_value):
        """Adds a new value to the current Circular Double Linked List (CDLL).
           Args:
           new_value: The value to be added to the list.
        """
        new_node = Node(new_value)
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.tail = new_node
        else:
            self.head.prev = new_node
            new_node.prev = self.tail
            self.tail.next = new_node
            new_node.next = self.head
            self.tail = new_node

    def return_first_element(self):
        """Returns the first element of the Circular Double Linked List (CDLL).
           Returns:
           The value of the first node in the CDLL. The return type will depend on the data type of the elements stored
           in the list.
        """
        self.current_value = self.head
        return self.head.value

    def return_next_element(self):
        """Returns the next element in the Circular Double Linked List (CDLL).
           Returns:
           The value of the next node in the CDLL. The return type will depend on the data type of the elements stored
           in the list.
        """
        self.current_value = self.current_value.next
        return self.current_value.value

    def return_prev_element(self):
        """Returns the previous element in the Circular Double Linked List (CDLL).
           Returns:
           The value of the previous node in the CDLL. The return type will depend on the data type of the elements
           stored in the list.
        """
        self.current_value = self.current_value.prev
        return self.current_value.value

    def delete(self):
        """Deletes the entire Circular Double Linked List (CDLL)."""
        self.head = None
        self.tail = None


class RoomsNamePictures:
    """Creates and manages two Circular Double Linked Lists (CDLLs), one for room names and the other for pictures.
       This implementation involves two distinct CDLLs: the first CDLL stores the names of rooms, while the second CDLL
       contains pictures associated with these rooms. The class or function provides mechanisms to add, remove, and
       traverse through these lists. It ensures that the operations on these lists maintain their circular and
       double-linked nature allowing for bidirectional traversal."""
    def __init__(self):
        self.rooms_name = CircularDoubleLinkedList()
        self.pictures = CircularDoubleLinkedList()

    def insert_room_names(self, rooms_name: list, db: Database):
        """Inserts all room names from an input string list into the 'rooms_name' CDLL, retrieves the first room name
           from this CDLL, and then updates the 'pictures' CDLL based on the first room's name.
           Args:
           rooms_name (list of str): A list of room names to be inserted into the 'rooms_name' CDLL.
           db: A reference to the database from which picture data for the rooms will be fetched.
        """
        # insert rooms names
        for room_name in rooms_name:
            self.rooms_name.add_new_value(room_name)
        # insert pictures for first room from rooms_name
        room_name = self.rooms_name.return_first_element()
        self.update_pictures_names(room_name, db)

    def return_initial_room_name(self):
        """Returns the initial room name from a data structure, typically from a collection or list where room names
           are stored.
           Returns:
           str: The name of the initial room in the collection.
        """
        return self.rooms_name.head.value

    def update_pictures_names(self, room_name: str, db: Database):
        """Updates the 'pictures' CDLL based on the specified room name. The update process involves several steps:
           1. Clear the current contents of the 'pictures' CDLL.
           2. Retrieve all pictures associated with the current room and store them in a list.
           3. Insert all pictures from the list into the now empty 'pictures' CDLL.
           4. Retrieve the first picture from the updated 'pictures' CDLL.
           5. Create a file named 'current_picture.png' in the 'current_image' folder based on the first picture
           from the 'pictures' CDLL.
           This method requires the room name to determine which pictures to fetch and a reference to the current
           database to access the picture data.
           Args:
           room_name (str): The name of the room for which pictures are to be updated in the CDLL.
           db: A reference to the current database to access picture data.
        """
        self.pictures.delete()
        all_pictures = db.get_pictures_from_room_with_name(room_name)
        for picture in all_pictures:
            self.pictures.add_new_value(picture)
        first_picture = self.pictures.return_first_element()
        db.write_to_file("current_image", f"current_picture.png", first_picture)

    def return_next_picture(self, db: Database):
        """Writes the 'new_picture' image into a file named 'current_picture.png'.
           Args:
           db: A reference to the current database from which the 'new_picture' image data is retrieved.
        """
        next_picture = self.pictures.return_next_element()
        db.write_to_file("current_image", f"current_picture.png", next_picture)

    def return_prev_picture(self, db: Database):
        """Writes the 'prev_picture' image into a file named 'current_picture.png'.
           Args:
           db: A reference to the current database from which the 'prev_picture' image data is retrieved.
        """
        prev_picture = self.pictures.return_prev_element()
        db.write_to_file("current_image", f"current_picture.png", prev_picture)

    def return_next_room_name(self, db: Database) -> str:
        """Returns the name of the next room from the 'rooms_name' Circular Double Linked List (CDLL).
           Args:
           db: A reference to the current database, which may be used for additional data retrieval if necessary.
           Returns:
           str: The name of the next room in the CDLL.
        """
        room_name = self.rooms_name.return_next_element()
        self.update_pictures_names(room_name, db)
        return room_name

    def return_prev_room_name(self, db: Database) -> str:
        """Returns the name of the previous room from the 'rooms_name' Circular Double Linked List (CDLL).
           Args:
           db: A reference to the current database, potentially used for supplementary data retrieval or validation.
           Returns:
           str: The name of the previous room in the CDLL.
        """

        room_name = self.rooms_name.return_prev_element()
        self.update_pictures_names(room_name, db)
        return room_name
