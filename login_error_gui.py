import tkinter
from tkinter import Toplevel, Label, PhotoImage, Button


class LoginError(Toplevel):
    """This class is responsible for creating and controlling the LoginErrorGui.
       It inherits from tkinter.Toplevel class."""
    def __init__(self, master_window: tkinter, error_cause: str):
        super().__init__(master=master_window)
        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
               created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
               intended to inform the user about the specific cause of the login error."""

        self.error_cause = error_cause
        self.master_window = master_window

        # disable master_window when current toplevel window is open
        self.master_window.attributes('-disabled', True)

        # set action when close button is pressed
        self.protocol("WM_DELETE_WINDOW", self.close_current_toplevel)

        self.title('Login Error')
        self.iconbitmap('icon/meeting.ico')
        self.geometry('650x200')
        self.resizable(False, False)

        self.background_label = Label(self, bg='white', width=400, height=200)
        self.background_label.place(x=0, y=0)

        self.error_image = PhotoImage(file='images/error_image.png')

        self.error_image_label = Label(self, image=self.error_image, background='white')
        self.error_image_label.place(x=50, y=50)

        self.error_message_label = Label(self, text=self.error_cause.center(60), font=('TimesNewRoman', 12),
                                         background='white', justify='center')
        self.error_message_label.place(x=170, y=50)

        self.ok_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc', text=' OK ',
                                font=('TimesNewRoman', 12), fg='black', activeforeground='black', width=10, height=2,
                                command=self.close_current_toplevel)
        self.ok_button.place(x=290, y=100)

        self.focus()

    def close_current_toplevel(self):
        """This method is responsible for re-enabling the top-level GUI and closing the LoginErrorGui window.
           It is typically called when the user has acknowledged the error message displayed in LoginErrorGui and the
           application needs to revert back to the main interactive window."""
        # enable master_window
        self.master_window.attributes('-disabled', False)
        self.destroy()


class NewScheduleGui(LoginError):
    """This class is responsible for creating and controlling the NewScheduleGui. It inherits from LoginError class."""
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)

        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error."""

        self.title('Schedule room')

        self.error_message_label.place(x=150, y=10)

        self.ok_button.place(x=250, y=120)
        self.ok_button.configure(command=self.ok_button_press)

        self.cancel_button = Button(self, bg='#529ffc', border=False, activebackground='#529ffc', text=' CANCEL ',
                                    font=('TimesNewRoman', 12), fg='black', activeforeground='black', width=10,
                                    height=2, command=self.close_current_toplevel)
        self.cancel_button.place(x=400, y=120)

    def ok_button_press(self):
        """This method enables toplevel gui, closes the NewScheduleGui and adds new schedule to the database."""
        self.close_current_toplevel()
        self.master_window.add_new_schedule_to_db()


class TimeSchedulePassedGui(LoginError):
    """This class is designed to create and manage the TimeSchedulePassedGui, a specialized user interface for handling
       scheduling errors. It inherits from the LoginError class, leveraging similar functionalities for displaying error
       messages and managing user interactions.
       The primary use of this class is to inform users when they attempt to create a schedule for the current day but
       choose a time interval that has already passed. The TimeSchedulePassedGui provides a clear and user-friendly
       notification about this specific scheduling conflict, guiding users to select a valid time interval."""
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)
        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error."""

        self.title('Time passed')


class EmailSendErrorGui(TimeSchedulePassedGui):
    """This class, EmailSendErrorGui, specializes in creating and controlling a graphical user interface (GUI) for
    handling errors encountered during the email sending process. It extends the TimeSchedulePassedGui class,
    inheriting its methods and attributes for error handling, but with a specific focus on email-related issues."""
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)
        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error."""

        self.title('Email Send Error')
        self.error_message_label.place(x=170, y=30)


class TokenExists(TimeSchedulePassedGui):
    """The TokenExistsGui class is designed to create and control a graphical user interface (GUI) specifically for
       scenarios where a user attempts to receive a token to reset their password, but a token already exists in the
       database. This class inherits from the TimeSchedulePassedGui class."""
    def __init__(self, master_window: tkinter, message: str, username: str, email_address: str):
        super().__init__(master_window, message)
        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error
           username (str): current username
           email_address (str): current user's email address"""

        self.username = username
        self.email_address = email_address

        self.title('Token already exists')
        self.error_message_label.place(x=170, y=30)
        self.ok_button.place(x=320, y=100)
        self.master_window = master_window
        self.ok_button.configure(command=self.ok_button_press)

    def close_current_toplevel(self):
        """This method enables toplevel gui and closes current the TokenExistsGui"""
        # enable master_window
        self.master_window.attributes('-disabled', False)
        self.destroy()

    def ok_button_press(self):
        """This method defines the sequence of actions that occur when the 'OK' button is pressed in the TokenExistsGui.
           It is responsible for managing the GUI windows and transitions as part of the user interaction flow.
           The method performs the following steps:
           1. Close the current TokenExistsGui window: This action dismisses the TokenExistsGui, removing it from the
           screen.
           2. Close the parent GUI window above which the TokenExistsGui was created: This ensures that the entire
           flow related to the token existence notification is concluded, and the user interface is cleared of these
           layers.
           3. Open the 'check token' window: This step initiates the next phase in the process, allowing the user to
           proceed with checking or validating the existing token."""

        self.close_current_toplevel()
        self.master_window.destroy()
        self.master_window.main_window.create_open_check_token_window(username=self.username,
                                                                      email_address=self.email_address)


class TokenDifferent(LoginError):
    """The TokenDifferentGui class specializes in creating and controlling a graphical user interface (GUI) for
       situations where there is a discrepancy between the token a user is attempting to use for password reset and
       the token that currently exists in the database. It inherits from the LoginError class, drawing on its error
       handling and display functionalities, while focusing specifically on token-related issues.

       The primary use of this class is to inform users in a clear and user-friendly manner about the mismatch of
       tokens. This situation typically occurs when a user requests a password reset token but the token they are
       trying to use differs from the one stored in the database, possibly due to a new token being generated in the
       interim."""
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)
        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error"""

        self.title('Different Tokens')


class PasswordDifferent(LoginError):
    """The PasswordDifferentGui class is designed to create and manage a graphical user interface (GUI) for handling
       situations where the password and the 'type password again' fields do not match during the creation of a new
       account. It inherits from the LoginError class, utilizing its capabilities to display error messages and manage
       user interactions in the context of password discrepancies.
    """
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)
        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error"""

        self.title('Different password')

        self.ok_button.place(x=320, y=100)


class PasswordUpdated(TimeSchedulePassedGui):
    """The PasswordUpdatedGui class specializes in creating and controlling a GUI to confirm the successful update of
       a user's password. This class inherits from the TimeSchedulePassedGui class, utilizing its infrastructure for
       GUI creation and management, but with a distinct focus on password update confirmations.
    """
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)

        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error"""

        self.title('Password Updated Successfully')
        self.error_message_label.place(x=170, y=30)
        self.ok_button.place(x=320, y=100)
        self.master_window = master_window
        self.ok_button.configure(command=self.ok_button_press)

    def close_current_toplevel(self):
        """This method enables toplevel gui and closes current PasswordUpdatedGui."""
        # enable master_window
        self.master_window.attributes('-disabled', False)
        self.destroy()

    def ok_button_press(self):
        """This method outlines the sequence of actions that are executed when the 'OK' button is pressed in the
           PasswordUpdatedGui. It manages the transition and flow of the user interface following a successful password
           update. The actions performed are as follows:
           1. Close the current PasswordUpdatedGui window.
           2. Close the parent GUI window above which the PasswordUpdatedGui was created.
           3. Open the login window."""
        self.close_current_toplevel()
        self.master_window.destroy()
        self.master_window.main_window.create_open_login_window()


class TokenExpiredDuringReset(PasswordUpdated):
    """The TokenExpiredDuringResetGui class is specifically developed to create and control a graphical user interface
       (GUI) in scenarios where a token used for password resetting expires during the update process. It inherits from
       the PasswordUpdated class, leveraging its functionalities for handling password update-related GUIs, but with a
       specific focus on token expiration issues."""
    def __init__(self, master_window: tkinter, message: str):
        super().__init__(master_window, message)

        """master_window (tkinter): The main application window or parent window over which the LoginErrorGui is 
           created.
           error_cause (str): The error message that will be displayed in the LoginErrorGui. This message is
           intended to inform the user about the specific cause of the login error"""

        self.title('Token Expired During Reset Process')
