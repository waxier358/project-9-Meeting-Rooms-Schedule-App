from login_window_gui import LoginWindow
from create_account_gui import CreateAccountWindow
from forgot_password_gui import ForgotPasswordWindow
from rooms_schedule_gui import RoomsSchedule
from check_token_gui import CheckTokenWindow
from reset_password_gui import ResetPasswordGui


class WindowManager:
    """Manages and controls the graphical user interface (GUI) components of the application.
    This class serves as the central manager for various GUI windows in the application. It is responsible for creating,
    initializing, and displaying different windows such as login, account creation, password reset, and room scheduling.
    """
    def __init__(self):
        self.create_login_window = None
        self.create_account_window = None
        self.create_forgot_password_window = None
        self.create_rooms_schedule_window = None
        self.create_check_token_window = None
        self.create_reset_password_gui_window = None

    def create_open_login_window(self):
        self.create_login_window = LoginWindow(self)
        self.create_login_window.mainloop()

    def create_open_account_window(self):
        self.create_account_window = CreateAccountWindow(self)
        self.create_account_window.mainloop()

    def create_open_forgot_password_window(self):
        self.create_forgot_password_window = ForgotPasswordWindow(self)
        self.create_forgot_password_window.mainloop()

    def create_open_check_token_window(self, username: str, email_address: str):
        self.create_check_token_window = CheckTokenWindow(self, username=username, email_address=email_address)
        self.create_check_token_window.mainloop()

    def create_open_rooms_schedule_window(self, username: str):
        self.create_rooms_schedule_window = RoomsSchedule(self, username=username)
        self.create_rooms_schedule_window.mainloop()

    def create_open_reset_password_window(self, username: str, email_address: str):
        self.create_reset_password_gui_window = ResetPasswordGui(self, username=username, email_address=email_address)
        self.create_reset_password_gui_window.mainloop()
