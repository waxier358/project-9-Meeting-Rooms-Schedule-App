import tkinter
from tkinter import PhotoImage, Label, Entry, Frame, Button, END
from datetime import datetime, timedelta

from check_fields import CheckFields
from db import Database
from login_error_gui import TokenExists
from send_email import sent_token_by_email
from utils import TOKEN_EXPIRATION_TIME


class ForgotPasswordWindow(tkinter.Tk):
    """This class creates and manages the 'Forgot Password Window'. This window is opened when the 'Forgot Password'
        button is pressed on the User Login Window."""

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.check_fields = CheckFields(self)
        self.db = Database()

        self.title('Meeting Rooms Schedule App - Forgot Password')
        self.resizable(False, False)
        self.geometry('1020x660')
        self.iconbitmap('icon/meeting.ico')

        self.background_image = PhotoImage(file='images/login_background.png')

        # create background and put background image in it
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0)

        # create account label
        self.user_login_label = Label(self, text='Forgot Password', border=False, fg='#529ffc',
                                      font=('TimesNewRoman', 23, 'bold'), background='white')
        self.user_login_label.place(x=710, y=100)

        # create email address entry
        self.email_entry = Entry(self, width=25, font=('TimesNewRoman', 15), border=False, fg='black')
        self.email_entry.insert(0, 'Email address')
        self.email_entry.place(x=700, y=310)

        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=340)

        # bind action on FocusIn event
        self.email_entry.bind('<FocusIn>', self.email_focus)

        # create receive_email button
        self.receive_email_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc',
                                           text='Receive token by Email',
                                           font=('TimesNewRoman', 12), fg='black', activeforeground='black', width=31,
                                           height=2, cursor='hand2', command=self.receive_token_by_email)
        self.receive_email_button.place(x=700, y=360)

        # bind action when ENTER is pressed
        self.bind('<Return>', self.receive_token_by_email)

    @staticmethod
    def convert_string_to_datetime(datetime_string: str) -> datetime:
        """Converts an input string representing a datetime into a datetime object.
           This function takes a string that represents a datetime in a specific format and converts it into a
           `datetime` object. The function assumes that the input string is formatted correctly according to a
           predefined datetime format. Proper error handling should be implemented to manage cases where the format is
           incorrect or the string cannot be converted.
           Args:
           datetime_string (str): The datetime string to be converted.
           Returns:
           datetime: A datetime object representing the input string.
        """
        return datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate_token_age(time_from_db: datetime) -> bool:
        """Checks if the current time is greater than the time associated with the current token from the database
           plus a predefined TOKEN_EXPIRATION_TIME.
           Args:
           time_from_db (datetime): The time associated with the current token, retrieved from the database.
           Returns:
           bool: True if the current time exceeds time_from_db plus TOKEN_EXPIRATION_TIME, False otherwise.
        """
        current_time = datetime.utcnow()
        token_maximum_age = timedelta(minutes=TOKEN_EXPIRATION_TIME)
        time_difference = current_time - time_from_db
        return time_difference < token_maximum_age

    def receive_token_by_email(self, event=None):
        """This method validates the syntax of an email address. If the syntax is incorrect, it generates an error
           message GUI. If the syntax is correct, the method retrieves a record from the users table in the database
           using the provided user's email address. If no matching record exists, it generates an error message GUI.
           If the email address exists in the database, the method proceeds to invoke another method for further
           processing.

           This method can be triggered by two actions:
           1. Pressing the ENTER key in the current GUI.
           2. Clicking the 'Receive token by email' button.
           Args:
           event (optional): A parameter used if the method is triggered by pressing the ENTER key.
        """
        # check if email format is ok
        email_check_ok = self.check_fields.check_email(self.email_entry.get().strip())
        # check if email exist in database
        if email_check_ok:
            get_email_from_database = self.db.get_user_by_email(self.email_entry.get().strip())
            # no email in database
            if not get_email_from_database:
                self.check_fields.no_email_address_exist(self.email_entry.get().strip())
            else:
                # email in database
                self.email_in_db_action(email_and_username_from_db=get_email_from_database)

    def email_in_db_action(self, email_and_username_from_db):
        """This method executes several tasks when an email address is found in the database:
           1. Retrieves the username and email address.
           2. Fetches the token associated with the username and email address from the database.
           3. If a current token exists:
                - Checks if the token is valid.
                - Handles both situations: if the token is valid or invalid.
           4. If no current token exists:
                - Creates a new token.
                - Sends the new token via email.
                - Opens the 'check token' GUI for further user interaction.
           Args:
           email_and_username_from_db (namedtuple): A namedtuple with fields 'id', 'username', 'email_address', 'salt',
                                                 and 'hash_of_password', containing the user's information retrieved
                                                 from the database.
        """
        # email in database
        username = email_and_username_from_db.username
        email_address = email_and_username_from_db.email_address
        # check if database contain a token associated with this username and email_address
        current_token = self.db.get_token_from_db(username=username, email_address=email_address)
        if current_token:
            # check if current token is valid
            if self.token_is_valid(token=current_token):
                # create an error window about already existing token
                self.handle_token_valid(username=username, email_address=email_address)
            else:
                # token is invalid
                self.handle_token_invalid(username=username, email_address=email_address)
        else:
            self.create_new_token_and_send_throw_email(username=username, email_address=email_address)
            self.close_current_window_and_open_check_token_gui(username=username, email_address=email_address)

    def handle_token_valid(self, username: str, email_address: str):
        """This method creates and displays a graphical user interface (GUI) for error messages.
           It is specifically designed to show error messages related to issues with a user's username or email address.
           Args:
           username (str): The username of the user for whom the error message is being generated.
           email_address (str): The email address of the user for whom the error message is being generated.
        """
        message = ("A valid token was already generated for this account!\n"
                   "Check email address and validate token on next window!")
        TokenExists(self, message=message, username=username, email_address=email_address)

    def handle_token_invalid(self, username: str, email_address: str):
        """This method addresses situations where a token is determined to be invalid. It performs the following tasks:
           1. Deletes the invalid token from the database.
           2. Creates a new token and sends it to the user via email.
           3. Opens the 'check token' GUI for user interaction to validate the new token.
           Args:
           username (str): The username associated with the invalid token. This is used for identifying the
                        specific user record in the database and for token regeneration purposes.
           email_address (str): The email address associated with the invalid token. This is used for sending
                             the newly generated token to the user.
        """
        # delete current token
        self.delete_token(username=username, email_address=email_address)
        # generate a new one, add in database and send in email address
        self.create_new_token_and_send_throw_email(username=username, email_address=email_address)
        self.close_current_window_and_open_check_token_gui(username=username, email_address=email_address)

    def token_is_valid(self, token) -> bool:
        """This method checks the validity of a given token and returns a boolean value indicating the result.
           It assesses whether the token is valid based on predefined criteria, such as expiration or matching records.
           Args:
           token (namedtuple): A namedtuple 'Token' containing the fields 'username', 'email_address', 'token',
                            and 'time_of_creation'. This namedtuple holds the necessary information to verify
                            the token's validity.
           Returns:
           bool: True if the token is valid, False otherwise. This boolean value indicates the result of the
           validity check.
        """
        time_from_db = self.convert_string_to_datetime(token.time_of_creation)
        return self.calculate_token_age(time_from_db=time_from_db)

    def close_current_window_and_open_check_token_gui(self, username: str, email_address: str):
        self.destroy()
        self.main_window.create_open_check_token_window(username=username, email_address=email_address)

    def create_new_token_and_send_throw_email(self, username: str, email_address: str):
        # create a token and add it in database and set start time
        new_token = self.create_and_get_new_token(username=username, email_address=email_address)
        # send email
        sent_token_by_email(destination_email_address=email_address, username=username, token=new_token.token)

    def create_and_get_new_token(self, username: str, email_address: str):
        """This method generates a new token associated with a given username and email address.
           It creates a unique token and records the time of its creation. The method returns this information in the
           form of a namedtuple.
           Args:
           username (str): The username for which the new token is being created. It is part of the information
                        encoded in the token.
           email_address (str): The email address associated with the username. This is also included in the token's
                             information.
           Returns:
           namedtuple: A namedtuple 'Token' containing the fields 'username', 'email_address', 'token', and
                    'time_of_creation'. This namedtuple encapsulates all relevant details of the newly created token."""
        self.db.create_new_token(username=username, email_address=email_address)
        return self.db.get_token_from_db(username=username, email_address=email_address)

    def delete_token(self, username: str, email_address: str):
        """This method removes a specific token from the tokens table in the database. It identifies and deletes the
           token based on the associated username and email address.
           Args:
           username (str): The username associated with the token to be deleted. This is used to locate the
                        specific token in the tokens table.
           email_address (str): The email address associated with the token to be deleted. Along with the username,
                             it helps in precisely identifying the correct token to remove."""
        self.db.delete_token_by_username_and_email_address(username=username, email_address=email_address)

    def email_focus(self, event):
        """This method defines the actions that are performed when a user clicks on an email entry."""
        if self.email_entry.get() == 'Email address':
            self.email_entry.delete(0, END)
