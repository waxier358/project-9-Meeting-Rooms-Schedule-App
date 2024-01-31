from string import ascii_lowercase, ascii_uppercase, digits, punctuation


from login_error_gui import LoginError


class CheckFields:
    """ A class used to check and validate user input fields.

    This class provides methods for validating the contents of various input fields, such as username and password.
    It checks for conditions like the presence of uppercase and lowercase letters, digits, and special
    characters in passwords and ensures that the username field is not empty. This class also provides feedback on
    errors using a GUI."""

    def __init__(self, window_name):
        # identify the name of the window to which the field belongs
        self.window_name = window_name

    @staticmethod
    def check_password_message(password: str, field_name: str = 'Password'):
        """Checks if a password contains uppercase, lowercase, digits, and special characters.

        Args:
        password: A string representing the password to be verified.
        field_name: (optional; default is 'Password')

        Returns:
        A string like 'Password has no uppercase character!' if a requirement is not met,
        or False if all requirements are satisfied.
        """
        if not any(map(lambda char: char in password, ascii_uppercase)):
            return f'{field_name} has no uppercase character!'
        elif not any(map(lambda char: char in password, ascii_lowercase)):
            return f'{field_name} has no uppercase lowercase character!'
        elif not any(map(lambda char: char in password, digits)):
            return f'{field_name} has no digit character!'
        elif not any(map(lambda char: char in password, punctuation)):
            return f'{field_name} has no special character'
        return False

    def check_username(self, username: str):
        """Checks if the username string is empty or contains only space characters.
        Opens a LoginError GUI if requirements are not met.

        Args:
        username: A string containing the username.

        Returns:
        None if the string is empty or contains only space characters,
        or True if all requirements are met.
        """
        if len(username) == 0:
            LoginError(self.window_name, error_cause='Username field is empty!')
            return
        elif len(username.strip()) == 0:
            LoginError(self.window_name, error_cause="Username field contains only ' ' !")
            return
        return True

    def check_password(self, password: str, field_name: str = 'Password'):
        """Checks if the password string is empty, contains only space characters, or is shorter than 8 characters.
        If these checks pass, it verifies if the string contains lowercase, uppercase, digits, and special characters.
        Opens a LoginError GUI if requirements are not met.

        Args:
        password: A string containing the password.
        field_name: (optional; default is 'Password')

        Returns:
        None if any of the requirements are not met,
        or True if all requirements are satisfied.
        """
        if len(password) == 0:
            LoginError(self.window_name, error_cause=f'{field_name} field is empty!')
            return
        elif len(password.strip()) == 0:
            LoginError(self.window_name, error_cause=f"{field_name} field contains only ' '!")
            return
        elif len(password.strip()) < 8:
            LoginError(self.window_name, error_cause=f"{field_name} must contain at least 8 characters!")
            return
        check_password_result = self.check_password_message(password.strip())
        if check_password_result:
            LoginError(self.window_name, error_cause=check_password_result)
            return
        return True

    def check_email(self, email: str):
        """Checks the syntax of an email address. An associated Login Error GUI is generated if any requirement is not
         met.

        Args:
        email: A string containing the email address.

        Returns:
        None if any requirement is not met,
        or True if all requirements are satisfied.
        """
        if len(email) == 0:
            LoginError(self.window_name, error_cause='Email address field is empty!')
            return
        elif len(email.strip()) == 0:
            LoginError(self.window_name, error_cause="Email address field contains only ' '!")
            return
        elif '@' not in email.strip():
            LoginError(self.window_name, error_cause="Email address must contain '@'!")
            return
        elif email.strip().count('@') >= 2:
            LoginError(self.window_name, error_cause="Email address must contain only one '@' char!")
            return
        elif email.strip()[-1] == '@':
            LoginError(self.window_name, error_cause="Enter a domain [username]@[domain]!")
            return
        elif email.strip()[0] == '@':
            LoginError(self.window_name, error_cause="Enter an username [username]@[domain]!")
            return
        email_and_domain = email.strip().split('@')
        if len(email_and_domain[1]) < 3:
            LoginError(self.window_name, error_cause="Domain length must be at least 3 chars [username]@[domain]!")
            return
        elif '.' not in email_and_domain[1]:
            LoginError(self.window_name, error_cause="Domain must contain '.' [username]@[domain]!")
            return
        elif email_and_domain[1][0] == '.':
            LoginError(self.window_name, error_cause="Subdomain must have at least 1 char! Email: [username]@[domain] "
                                                     "domain:[subdomain].[top-level domain]")
            return
        elif email_and_domain[1][-1] == '.':
            LoginError(self.window_name, error_cause="Top level domain must have at least 2 chars [username]@[domain]!")
            return
        subdomain_and_top_level_domain = email_and_domain[1].split('.')
        if len(subdomain_and_top_level_domain[1]) < 2:
            LoginError(self.window_name, error_cause="Top level domain must have at least 2 chars [username]@[domain]!")
            return
        return True

    def check_password_and_again_password(self, password: str, again_password: str):
        """Checks if two input strings are the same. Generates a Login Error GUI if the inputs differ.

        Args:
        password: String from the password entry field.
        again_password: String from the repeat password entry field.

        Returns:
        None if the inputs differ,
        or True if the inputs are the same.
        """
        if password != again_password:
            LoginError(self.window_name, error_cause="Password and Type Password Again must be the same!")
            return
        return True

    def username_exist(self, username: str):
        """Generates a LoginError GUI if the input username string exists in the database."""
        LoginError(self.window_name, error_cause=f"Username {username} already exists!")

    def no_username_exist(self, username: str):
        """Generates a LoginError GUI if the input username does not exist in the database."""
        LoginError(self.window_name, error_cause=f"Username {username} doesn't exist!")

    def email_address_exist(self, email_address: str):
        """Generates a LoginError GUI if an account with the input email address exists in the database."""
        LoginError(self.window_name, error_cause=f"An account with email address {email_address} already exists!")

    def no_email_address_exist(self, email_address: str):
        """Generates a LoginError GUI if an account with the input email address does not exist in the database."""
        LoginError(self.window_name, error_cause=f"An account with email address {email_address} doesn't exist!")

    def user_registered_correct(self):
        """Generates a LoginError GUI for the newly created account."""
        LoginError(self.window_name, error_cause=f"An account was created! Please login!")

    def incorrect_password(self):
        """Generates a LoginError GUI if an incorrect password is entered."""
        LoginError(self.window_name, error_cause=f"Incorrect password! Try again!")
