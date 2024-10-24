class NotPositiveIntegerValueError(Exception):
    """
    An exception class to handle errors when a non-positive integer value is input.

    Methods:
        __str__(): Returns an error message indicating that the input was incorrect.

    Usage:
        Raises this exception when a non-positive integer input is encountered.
    """

    def __str__(self):
        return 'Error! Incorrect Input. Try again: '


class InvalidOptionError(Exception):
    """
    An exception that is raised when an invalid option is encountered.

    Methods:
        __str__(): Returns a string representation of the error message.
    """

    def __str__(self):
        return 'Incorrect option'
