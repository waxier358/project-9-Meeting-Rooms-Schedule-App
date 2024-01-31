import yagmail

GMAIL_APP_PWD = 'your_password'
EMAIL_ADDRESS = 'your_email_address@gmail.com'


def prep_and_send_email_schedule_information(destination_email_address: str,  room_name: str, order_date: str,
                                             order_interval: str):
    """Prepares and sends an email with schedule information to the specified recipient.

    This function composes an email containing details of a scheduled booking and sends it to the destination email
    address. The email includes information such as the room name, date, and time interval of the scheduled booking.
    Args:
        destination_email_address (str): The email address of the recipient (current user) to whom the schedule
        information is to be sent.
        room_name (str): The name of the room that has been scheduled.
        order_date (str): The date on which the room is scheduled.
        order_interval (str): The time interval during which the room is booked.
    Note:
        The function assumes that an email sending mechanism (like SMTP server details) is already configured and
        available for sending the email.
     """
    yag = yagmail.SMTP(EMAIL_ADDRESS, GMAIL_APP_PWD)

    content = (f"Greetings from Meetings Rooms Schedule App!!!\n"
               f"You have a schedule for {room_name} on {order_date} at {order_interval}.\n"
               f"Wish you all the best!!!")

    yag.send(destination_email_address, "Meeting Rooms Scheduler Application", content)


def sent_token_by_email(destination_email_address: str, username: str, token: str):
    """Prepares and sends an email with a password reset token to the specified user.
    This function composes an email containing a token that allows the user to reset their password. The email is sent
    to the provided destination email address. The email includes the username and the token, and it typically contains
    instructions on how to use the token for password resetting.
    Args:
        destination_email_address (str): The email address of the user who is to receive the password reset token.
        username (str): The username of the user who is resetting their password.
        token (str): The token that enables the user to reset their password.
    Note:
        The function assumes that an email delivery system (such as an SMTP server) is properly configured and
         accessible for sending the email.
    """
    yag = yagmail.SMTP(EMAIL_ADDRESS, GMAIL_APP_PWD)

    content = (f"Greetings from Meetings Rooms Schedule App!!!\n"
               f"To reset your password for username {username} use this token:\n\n"
               f"{token}\n\n"
               f"Wish you all the best!!!")

    yag.send(destination_email_address, "Meeting Rooms Scheduler Application Reset Password", content)
