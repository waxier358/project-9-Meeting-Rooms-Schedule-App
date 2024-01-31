class EmailSendException(Exception):
    """ Defines a custom exception class for handling errors that occur during email sending operations.
        This class inherits from the built-in Exception class and is designed to encapsulate the unique error scenarios
        encountered while performing email send operations. It can be used to catch and handle specific exceptions
        related to email functionality, allowing for more precise error handling and messaging in the context of email
         operations."""
    def __init__(self):
        super().__init__()
