import tkinter
from tkinter import PhotoImage, Label, Entry, Frame, END, Button

import bcrypt

from check_fields import CheckFields
from db import Database


class LoginWindow(tkinter.Tk):
    """Create and control login window."""

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.check_fields = CheckFields(self)
        self.db = Database()

        self.title('Meeting Rooms Schedule App - User Login')
        self.resizable(False, False)
        self.geometry('1020x660')
        self.iconbitmap('icon/meeting.ico')

        self.background_image = PhotoImage(file='images/login_background.png')

        # create background and put background image in it
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0)
        # create user login label
        self.user_login_label = Label(self, text='User Login', border=False, fg='#529ffc',
                                      font=('TimesNewRoman', 23, 'bold'), background='white')
        self.user_login_label.place(x=750, y=100)

        # create username entry
        self.username_entry = Entry(self, width=25, font=('TimesNewRoman', 15), border=False, fg='black')
        self.username_entry.insert(0, 'Username')
        self.username_entry.place(x=700, y=200)

        # bind action on FocusIn event
        self.username_entry.bind('<FocusIn>', self.username_focus)

        # bind action when ENTER is pressed
        self.bind('<Return>', self.check_username_and_password_syntax)
        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=230)

        # create password entry
        self.password_entry = Entry(self, width=23, font=('TimesNewRoman', 15), border=False, fg='black')
        self.password_entry.insert(0, 'Password')
        self.password_entry.place(x=700, y=250)
        self.password_entry.bind('<FocusIn>', self.password_focus)

        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=280)
        # create show-hide button and bind action
        self.show_password_image = PhotoImage(file='images/show_password.png')
        self.hide_password_image = PhotoImage(file='images/hide_password.png')
        self.password_button = Button(self, image=self.show_password_image, bg='white', border=False,
                                      activebackground='white', cursor='hand2', command=self.hide_password)
        self.password_button.place(x=950, y=250)

        # create forgot password button
        self.forgot_password_button = Button(self, bg='white', border=False, activebackground='white', cursor='hand2',
                                             text='Forgot Password', font=('TimesNewRoman', 12), fg='#529ffc',
                                             activeforeground='#529ffc', command=self.click_forgot_password)
        self.forgot_password_button.place(x=855, y=300)

        # create login button
        self.login_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc', text='Login',
                                   font=('TimesNewRoman', 12), fg='black', activeforeground='black', width=31, height=2,
                                   cursor='hand2', command=self.check_username_and_password_syntax)
        self.login_button.place(x=700, y=350)

        # create don't have an account label
        self.no_account_label = Label(self, text="Don't have an account?", border=False, fg='black',
                                      font=('TimesNewRoman', 12), background='white')
        self.no_account_label.place(x=700, y=420)

        # create new account button
        self.create_account_button = Button(self, bg='white', border=False, activebackground='white',
                                            text='Create new one', font=('TimesNewRoman', 12), fg='#529ffc',
                                            activeforeground='#529ffc', cursor='hand2',
                                            command=self.access_create_account_window)
        self.create_account_button.place(x=865, y=415)

    def username_focus(self, event):
        """Action performed when user click on username entry field."""
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0, END)

    def password_focus(self, event):
        """Action performed when user click on password entry field"""
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0, END)

    def hide_password(self):
        """Hide password from password entry field when user press self.password_button."""
        self.password_button.config(image=self.hide_password_image, command=self.show_password)
        self.password_entry.config(show='*')

    def show_password(self):
        """Show password from password entry field when user press self.password_button."""
        self.password_button.config(image=self.show_password_image, command=self.hide_password)
        self.password_entry.config(show='')

    def access_create_account_window(self):
        """Action performed when user press Create new one(account) """
        self.destroy()
        self.main_window.create_open_account_window()

    def check_username_and_password_syntax(self, event=None):
        """
        Checks the syntax of the username and password.

        This method validates the syntax of the username first, and then the syntax of the password. If both are
        correct, it proceeds with further functionality. The process stops if either check fails. This method can be
        triggered by two actions:
        1. Pressing the ENTER key in the current GUI.
        2. Clicking the Login button.

        Args:
            event (optional): A parameter used if the method is triggered by pressing ENTER.
        """
        if self.check_username():
            if self.check_password():
                self.handle_correct_username_and_password_syntax()
            else:
                return
        else:
            return

    def handle_correct_username_and_password_syntax(self):
        """Action performed if username syntax and password syntax are correct.

        Extract a namedtuple ('user_salt_and_password', 'username salt hash_of_password') from database based on
        username provided in username_entry. If such data does not exist, it implies that the username
        from username_entry is not in the database. Depending on the existence of the username in the database,
        appropriate actions are performed.
        """
        user_salt_hash_of_password = (self.db.get_salt_and_password_by_username_email
                                      (username=self.username_entry.get().strip()))
        # check if username from username_entry is in database
        if not user_salt_hash_of_password:
            # no username
            self.check_fields.no_username_exist(username=self.username_entry.get().strip())
        else:
            # username in database
            self.handle_username_exist_in_db(user_salt_hash_of_password=user_salt_hash_of_password)

    def handle_username_exist_in_db(self, user_salt_hash_of_password):
        """Action performed when username from username_entry exists in database.

        Verify if password from password_entry in byte string format match hash associated with current username in
        database. Depending on this match appropriate actions are performed.

        Args:
            user_salt_hash_of_password (User_salt_and_hash): A namedtuple representing the user's username, salt,
            hash_of_password. The namedtuple structure is defined as namedtuple('user_salt_and_password', 'username salt
            hash_of_password')
        """
        entered_password = self.password_entry.get().strip().encode('utf-8')

        result = bcrypt.checkpw(entered_password, user_salt_hash_of_password.hash_of_password)
        if not result:
            self.check_fields.incorrect_password()
        else:
            self.handle_correct_entered_password()

    def handle_correct_entered_password(self):
        """Action performed when password from password entry field match password from database associated
        with current username"""
        username = self.username_entry.get().strip()
        self.destroy()
        self.main_window.create_open_rooms_schedule_window(username=username)

    def check_username(self):
        """Checks username syntax.

        Returns:
            bool: True if username syntax is correct else return False
        """
        return self.check_fields.check_username(self.username_entry.get())

    def check_password(self):
        """Checks password syntax.

        Returns:
            bool: True if password syntax is correct else return False
        """
        return self.check_fields.check_password(self.password_entry.get())

    def click_forgot_password(self):
        """Action performed when user click forgot password """
        self.destroy()
        self.main_window.create_open_forgot_password_window()
