from datetime import datetime, timedelta
from utils import TOKEN_EXPIRATION_TIME


class TimeOperations:
    """Provides an environment for time-related operations.
    This class is designed to handle various time operations such as converting string representations of dates and
    times to datetime objects and calculating the age of tokens based on timestamps.
    Args:
        datetime_string (str): A datetime value in string format (e.g., "YYYY-MM-DD HH:MM:SS").
    """
    def __init__(self, datetime_string: str):
        self.datetime_string = datetime_string

    @staticmethod
    def calculate_token_age(time_from_db: datetime) -> bool:
        """Checks if the time elapsed between a given time from the database and the current time is less than the
        predefined TOKEN_EXPIRATION_TIME.

        Args:
            time_from_db (datetime): The time from the database, typically the creation time of a token.

        Returns:
            bool: True if the time difference is less than TOKEN_EXPIRATION_TIME, otherwise False.

        Note:
            TOKEN_EXPIRATION_TIME should be defined elsewhere in the code (e.g., as a constant).
        """
        current_time = datetime.utcnow()
        token_maximum_age = timedelta(minutes=TOKEN_EXPIRATION_TIME)
        time_difference = current_time - time_from_db
        return time_difference < token_maximum_age

    def convert_string_to_datetime(self):
        """Converts the datetime string (stored in the instance attribute) to a datetime object.
        Returns:
            datetime: The datetime object representing the datetime_string attribute."""
        return datetime.strptime(self.datetime_string, "%Y-%m-%d %H:%M:%S")
