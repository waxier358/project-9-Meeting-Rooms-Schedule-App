import tkinter
from tkinter import PhotoImage, Label, Entry, Frame, END, Button
from db import Database
from login_error_gui import TokenDifferent


class CheckTokenWindow(tkinter.Tk):
    """Creates and controls the check token window."""
    def __init__(self, main_window, username, email_address):
        super().__init__()

        self.main_window = main_window
        self.db = Database()

        self.username = username
        self.email_address = email_address
        self.token_from_db = None
        self.token_from_gui = None

        self.title('Meeting Rooms Schedule App - Check Token')
        self.resizable(False, False)
        self.geometry('1020x660')
        self.iconbitmap('icon/meeting.ico')

        self.background_image = PhotoImage(file='images/login_background.png')

        # create background and put background image in it
        self.background_label = Label(self, image=self.background_image)
        self.background_label.place(x=0, y=0)

        # create account label
        self.user_login_label = Label(self, text='Check Token', border=False, fg='#529ffc',
                                      font=('TimesNewRoman', 23, 'bold'), background='white')
        self.user_login_label.place(x=710, y=100)

        # create email address entry
        self.token_entry = Entry(self, width=27, font=('TimesNewRoman', 15), border=False, fg='black')
        self.token_entry.insert(0, 'Token')
        self.token_entry.place(x=700, y=310)

        # create frame
        Frame(self, width=285, height=2, bg='black').place(x=700, y=340)

        # bind action on FocusIn event
        self.token_entry.bind('<FocusIn>', self.token_focus)

        # create receive_email button
        self.check_token_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc',
                                         text='Check token', font=('TimesNewRoman', 12), fg='black',
                                         activeforeground='black', width=31, height=2,
                                         cursor='hand2', command=self.check_token_button_click)
        self.check_token_button.place(x=700, y=360)

        # bind action on FocusIn event
        self.bind('<Return>', self.check_token_button_click)

    def token_focus(self, event):
        """Action performed when the user clicks on token entry field."""
        if self.token_entry.get() == 'Token':
            self.token_entry.delete(0, END)

    def check_token_button_click(self, event=None):
        """
        Checks the token provided by the user against the token associated with the user in the database.
        This method can be triggered by two actions:
        Pressing the ENTER key within the current GUI.
        Clicking the 'Check Token' button.
        Args:
        event (optional): A parameter used when the method is triggered by pressing the ENTER key.
        """
        self.token_from_gui = self.token_entry.get().strip()
        # check token
        if self.check_if_gui_token_and_token_from_db_is_same():
            # same tokens_action
            self.handle_same_token()
        else:
            # different token action
            self.handle_different_token()

    def check_if_gui_token_and_token_from_db_is_same(self) -> bool:
        """Retrieves the token associated with a username from the database and compares it with the token entered by
        the user in the GUI.

        Returns:
        True if the tokens match, False otherwise."""
        self.token_from_db = self.db.get_token_from_db(username=self.username, email_address=self.email_address)
        return self.token_from_gui == self.token_from_db.token

    def handle_same_token(self):
        """Closes the current GUI and opens the reset password GUI."""
        self.close_current_gui_open_reset_password()

    def handle_different_token(self):
        """Generates an error GUI when the tokens do not match."""
        message = 'You entered a wrong token!'
        TokenDifferent(self, message=message)

    def close_current_gui_open_reset_password(self):
        """Close the current GUI and opens reset password GUI."""
        self.destroy()
        self.main_window.create_open_reset_password_window(username=self.username, email_address=self.email_address)
