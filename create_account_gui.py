import sqlite3
import tkinter
from tkinter import PhotoImage, Label, Entry, Frame, Button, END

from check_fields import CheckFields
from db import Database


class CreateAccountWindow(tkinter.Tk):
    """This class creates and manages the 'Create Account Window'. This window is opened when the 'Create new one'
    button is pressed on the User Login Window."""

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.check_fields = CheckFields(self)
        self.db = Database()

        self.title('Meeting Rooms Schedule App - Create Account')
        self.resizable(False, False)
        self.geometry('1020x660')
        self.iconbitmap('icon/meeting.ico')

        self.background_image = PhotoImage(file='images/login_background.png')

        # create background and put background image in it
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0)

        # create account label
        self.user_login_label = Label(self, text='Create Account', border=False, fg='#529ffc',
                                      font=('TimesNewRoman', 23, 'bold'), background='white')
        self.user_login_label.place(x=720, y=100)

        # create username entry
        self.username_entry = Entry(self, width=25, font=('TimesNewRoman', 15), border=False, fg='black')
        self.username_entry.insert(0, 'Username')
        self.username_entry.place(x=700, y=200)

        # bind action on FocusIn event
        self.username_entry.bind('<FocusIn>', self.username_focus)

        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=230)

        # create email address entry
        self.email_entry = Entry(self, width=25, font=('TimesNewRoman', 15), border=False, fg='black')
        self.email_entry.insert(0, 'Email address')
        self.email_entry.place(x=700, y=250)
        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=280)

        # bind action on FocusIn event
        self.email_entry.bind('<FocusIn>', self.email_focus)

        # create password entry
        self.password_entry = Entry(self, width=23, font=('TimesNewRoman', 15), border=False, fg='black')
        self.password_entry.insert(0, 'Password')
        self.password_entry.place(x=700, y=300)
        self.password_entry.bind('<FocusIn>', self.password_focus)

        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=330)

        # create show-hide button and bind action
        self.show_password_image = PhotoImage(file='images/show_password.png')
        self.hide_password_image = PhotoImage(file='images/hide_password.png')
        self.password_button = Button(self, image=self.show_password_image, bg='white', border=False,
                                      activebackground='white', cursor='hand2', command=self.hide_password)
        self.password_button.place(x=950, y=300)

        # create type password again entry
        self.again_password_entry = Entry(self, width=23, font=('TimesNewRoman', 15), border=False, fg='black')
        self.again_password_entry.insert(0, 'Type Password Again')
        self.again_password_entry.place(x=700, y=350)
        self.again_password_entry.bind('<FocusIn>', self.again_password_focus)

        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=380)

        # create show-hide button and bind action
        self.again_password_button = Button(self, image=self.show_password_image, bg='white', border=False,
                                            activebackground='white', cursor='hand2', command=self.hide_again_password)
        self.again_password_button.place(x=950, y=350)

        # create login button
        self.login_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc', text='Register',
                                   font=('TimesNewRoman', 12), fg='black', activeforeground='black', width=31, height=2,
                                   cursor='hand2', command=self.check_all_entry_fields)
        self.login_button.place(x=700, y=420)

        # bind action when ENTER is pressed
        self.bind('<Return>', self.check_all_entry_fields)

    def username_focus(self, event):
        """Action performed when the user clicks on username entry field."""
        if self.username_entry.get() == 'Username':
            self.username_entry.delete(0, END)

    def password_focus(self, event):
        """Action performed when user clicks on the password entry field."""
        if self.password_entry.get() == 'Password':
            self.password_entry.delete(0, END)

    def email_focus(self, event):
        """Action performed when the user clicks on email entry field."""
        if self.email_entry.get() == 'Email address':
            self.email_entry.delete(0, END)

    def again_password_focus(self, event):
        """Action performed when the user clicks on the 'again_password' entry field."""
        if self.again_password_entry.get() == 'Type Password Again':
            self.again_password_entry.delete(0, END)

    def hide_password(self):
        """Action performed when the user clicks on the password button."""
        self.password_button.config(image=self.hide_password_image, command=self.show_password)
        self.password_entry.config(show='*')

    def show_password(self):
        """Action performed when the user clicks on the password button."""
        self.password_button.config(image=self.show_password_image, command=self.hide_password)
        self.password_entry.config(show='')

    def hide_again_password(self):
        """Action performed when the user clicks on the password button."""
        self.again_password_button.config(image=self.hide_password_image, command=self.show_again_password)
        self.again_password_entry.config(show='*')

    def show_again_password(self):
        """Action performed when the user clicks on again password button."""
        self.again_password_button.config(image=self.show_password_image, command=self.hide_again_password)
        self.again_password_entry.config(show='')

    def check_all_entry_fields(self, event=None):
        """
        Checks the syntax of username, email, password, and 'again_password'.

        This method validates the syntax of the username, email, password and 'again_password' fields individually.
        If any of these fields fail validation, the method triggers an error message GUI.
        If the syntax of all the specified fields is correct, the method further verifies whether the password and
        'again_password' are identical. If all requirements are satisfied, the method registers the new username,
        new email and new password in the database. However, if a record with the new username and new email address
        already exists, this method will generate an error message GUI; otherwise, it closes the current window and
        opens the login window.
        This method can be triggered by two actions:
        1. Pressing the ENTER key in the current GUI.
        2. Clicking the 'Register' button.

        Args:
        event (optional): A parameter used if the method is triggered by pressing the ENTER key.
        """
        email_check_ok, password_check_ok, again_password_check_ok, check_password_and_again_password_ok = (False,
                                                                                                            False,
                                                                                                            False,
                                                                                                            False)

        username_check_ok = self.check_fields.check_username(self.username_entry.get())
        if username_check_ok:
            email_check_ok = self.check_fields.check_email(self.email_entry.get())
        if email_check_ok:
            password_check_ok = self.check_fields.check_password(password=self.password_entry.get(),
                                                                 field_name='Password')
        if password_check_ok:
            again_password_check_ok = self.check_fields.check_password(password=self.again_password_entry.get(),
                                                                       field_name='Type Password Again')
        if again_password_check_ok:
            check_password_and_again_password_ok = (self.check_fields.check_password_and_again_password
                                                    (password=self.password_entry.get(),
                                                     again_password=self.again_password_entry.get()))
        if check_password_and_again_password_ok:

            try:
                self.db.add_new_user_to_db(username=self.username_entry.get().strip(),
                                           email_address=self.email_entry.get().strip(),
                                           password=self.password_entry.get().strip())
            except sqlite3.IntegrityError as err:
                if 'username' in err.args[0]:
                    self.check_fields.username_exist(self.username_entry.get().strip())
                elif 'email_address' in err.args[0]:
                    self.check_fields.email_address_exist(self.email_entry.get().strip())
            else:
                self.destroy()
                self.main_window.create_open_login_window()
