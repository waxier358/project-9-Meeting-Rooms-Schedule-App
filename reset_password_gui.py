import tkinter
from tkinter import PhotoImage, Label, Entry, Frame, END, Button
from db import Database
from login_error_gui import PasswordDifferent, PasswordUpdated, TokenExpiredDuringReset
from check_fields import CheckFields
from time_operations import TimeOperations


class ResetPasswordGui(tkinter.Tk):
    """This class create and control ResetPasswordGui. It is inherited from tkinter.TK"""
    def __init__(self, main_window: tkinter, username: str, email_address: str):
        super().__init__()
        """Args:
               master_window: window manager
               username: str, current username
               email_address: str, current email_address
        """
        self.main_window = main_window
        self.db = Database()

        self.username = username
        self.email_address = email_address
        self.check_fields = CheckFields(self)

        self.title('Meeting Rooms Schedule App - Reset Password')
        self.resizable(False, False)
        self.geometry('1020x660')
        self.iconbitmap('icon/meeting.ico')

        self.background_image = PhotoImage(file='images/login_background.png')

        # create background and put background image in it
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0)

        # create account label
        self.user_login_label = Label(self, text='Reset Password', border=False, fg='#529ffc',
                                      font=('TimesNewRoman', 23, 'bold'), background='white')
        self.user_login_label.place(x=710, y=100)

        # create password entry
        self.new_password_entry = Entry(self, width=23, font=('TimesNewRoman', 15), border=False, fg='black')
        self.new_password_entry.insert(0, 'New Password')
        self.new_password_entry.place(x=700, y=290)
        self.new_password_entry.bind('<FocusIn>', self.new_password_focus)

        Frame(self, width=280, height=2, bg='black').place(x=700, y=320)

        # create show-hide button and bind action
        self.show_new_password_image = PhotoImage(file='images/show_password.png')
        self.hide_new_password_image = PhotoImage(file='images/hide_password.png')
        self.new_password_button = Button(self, image=self.show_new_password_image, bg='white', border=False,
                                          activebackground='white', cursor='hand2', command=self.hide_new_password)
        self.new_password_button.place(x=950, y=290)

        # create type password again entry
        self.again_new_password_entry = Entry(self, width=23, font=('TimesNewRoman', 15), border=False, fg='black')
        self.again_new_password_entry.insert(0, 'Type Password Again')
        self.again_new_password_entry.place(x=700, y=340)
        self.again_new_password_entry.bind('<FocusIn>', self.again_new_password_focus)

        # create frame
        Frame(self, width=280, height=2, bg='black').place(x=700, y=370)

        # create show-hide button and bind action
        self.again_new_password_button = Button(self, image=self.show_new_password_image, bg='white', border=False,
                                                activebackground='white', cursor='hand2',
                                                command=self.hide_again_new_password)
        self.again_new_password_button.place(x=950, y=340)

        # create reset button
        self.reset_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc', text='Reset Password',
                                   font=('TimesNewRoman', 12), fg='black', activeforeground='black', width=31, height=2,
                                   cursor='hand2', command=self.reset_password)
        self.reset_button.place(x=700, y=390)

        # bind action an ENTER pressed
        self.bind('<Return>', self.reset_password)

    def new_password_focus(self, event):
        """Action performed when user click on new_password_entry."""
        if self.new_password_entry.get() == 'New Password':
            self.new_password_entry.delete(0, END)

    def again_new_password_focus(self, event):
        """Action performed when user click on again_new_password_entry."""
        if self.again_new_password_entry.get() == 'Type Password Again':
            self.again_new_password_entry.delete(0, END)

    def hide_new_password(self):
        """Action performed when user click on new_password_button."""
        self.new_password_button.config(image=self.hide_new_password_image, command=self.show_new_password)
        self.new_password_entry.config(show='*')

    def show_new_password(self):
        """Action performed when user click on new_password_button."""
        self.new_password_button.config(image=self.show_new_password_image, command=self.hide_new_password)
        self.new_password_entry.config(show='')

    def hide_again_new_password(self):
        """Action performed when user click on again_new_password_button."""
        self.again_new_password_button.config(image=self.hide_new_password_image, command=self.show_again_password)
        self.again_new_password_entry.config(show='*')

    def show_again_password(self):
        """Action performed when user click on again_new_password_button."""
        self.again_new_password_button.config(image=self.show_new_password_image, command=self.hide_again_new_password)
        self.again_new_password_entry.config(show='')

    def reset_password(self, event=None):
        """This method checks if new_password and type_password_again is same or not.
        This method can be triggered by two actions:
        1. Pressing the ENTER key in the current GUI.
        2. Clicking the Reset Password button.

        Args:
            event (optional): A parameter used if the method is triggered by pressing ENTER.
        """
        # check if password and type_again are the same
        if self.is_same_password():
            self.handle_same_password()
        else:
            self.handle_diff_password()

    def is_same_password(self) -> bool:
        """Returns True or False if new_password_entry is same as again_new_password_entry."""
        return self.new_password_entry.get().strip() == self.again_new_password_entry.get().strip()

    def handle_same_password(self):
        """This method handles situations where the current password and the new password are the same:
        1. Verifies the syntax of the password. If the syntax is incorrect, a MessageErrorGui is displayed.
        2. If the syntax is correct, the method then checks the validity of the token. It handles scenarios for both
         valid and invalid tokens."""
        if self.check_password_fields():
            # check if token is valid
            current_token_time_string = self.db.get_token_from_db(username=self.username,
                                                                  email_address=self.email_address).time_of_creation
            current_token_time_datetime = (TimeOperations(datetime_string=current_token_time_string).
                                           convert_string_to_datetime())
            if (TimeOperations(datetime_string=current_token_time_datetime).calculate_token_age
                    (current_token_time_datetime)):
                # token is valid
                self.handle_valid_token()
            else:
                # token invalid
                self.handle_invalid_token()

    def handle_valid_token(self):
        """This method handles the situation when the token is valid:

        1. Updates the password for the current username in the database.
        2. Deletes the token associated with the current username from the token table in the database.
        3. Displays a message indicating successful password update."""
        # update password in database
        self.db.update_password(username=self.username, email_address=self.email_address,
                                password=self.new_password_entry.get().strip())
        # delete current_token
        self.db.delete_token_by_username_and_email_address(username=self.username, email_address=self.email_address)
        # open login window
        message = (f'Password for username {self.username} was updated!\n'
                   f'Login Again with new password.')
        PasswordUpdated(self, message=message)

    def handle_invalid_token(self):
        """ This method handles the response when the token is invalid:
        Creates and displays a message indicating that the token is invalid."""
        message = (f'During reset password process for {self.username}\n'
                   f'associated token expired! Try again!')
        TokenExpiredDuringReset(self, message=message)

    def check_password_fields(self) -> bool or None:
        """Checks the syntax of the value from an entry field.
        Returns:
            bool: True if the syntax of the entered value is correct.
            None: If the syntax of the entered value is incorrect."""
        checking_result = self.check_fields.check_password(password=self.new_password_entry.get().strip(),
                                                           field_name='New Password')
        return checking_result

    def handle_diff_password(self):
        """Creates a MessageErrorGui when the current password and the new password are different."""
        message = 'New Password and Type Password Again are different!'
        PasswordDifferent(self, message=message)
