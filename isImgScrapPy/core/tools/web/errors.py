from isImgScrapPy.core.errors import isImgScrapPyError, CHILD_PREFIX


class RemoteFileNotFoundError(isImgScrapPyError):
    message = "Remote File Not Found:\n    The specified address returned a response of '404 - Page Not Found'."
    prefix = CHILD_PREFIX

    def __init__(self, message=None, skip_print=None, url=None):
        self.message += f' [{url}]' if url is not None else '!'

        self.message = f"[{self.__class__.__name__}] - {self.message}"
        message = f"{self.prefix}- {message}" if message is not None else ''
        self.message += message
        super(RemoteFileNotFoundError, self).__init__(message=self.message, skip_print=skip_print)


class URLValidationError(isImgScrapPyError):
    """ Raised when a URL is found invalid. """
    message = "URL Validation Failed:\n    Unable to validate URL!"
    prefix = CHILD_PREFIX

    def __init__(self, message=None, skip_print=False, url=None, status_code=None):
        """ Raise a new instance of :class:`URLValidationError`.

        Raises a new instance of the :class:`URLValidationError` exception.

        Parameters:
            message (Optional[str]):
                The message to display during exception. (Defaults to None)

            skip_print (Optional[bool]):
                Should the exception message be printed to the console?

                    * If set to True, the exception message is not printed during raise.

                    * If set to False, the exception message is printed to the console during raising.
                    (Default behavior)

        Attributes:
            message (str):
                The message to pass for displaying upon raise.
        """

        self.message += f' [{url}]' if url is not None else '!'
        self.message = f"[{self.__class__.__name__}] - {self.message}"
        message = f"{self.prefix}- {message}" if message is not None else ''
        self.message += message
        super(URLValidationError, self).__init__(message=self.message, skip_print=skip_print)


class AttributeNotSetError(isImgScrapPyError):
    # Let's set a more specific message for the child exception.
    message = "Attribute Not Set Error - This attribute has not been set.\n    The requested attribute hasn't been "\
              "set in this instance."
    prefix = CHILD_PREFIX

    def __init__(self, message=None, skip_print=False, attribute_name=None):

        attr_desc = f" | {attribute_name} |" if attribute_name else ''
        # Prettify our base message string.
        self.message = f"[{self.__class__.__name__}]{attr_desc} - {self.message}"

        message = f"{self.prefix} - {message}" if message is not None else ''

        self.message += message

        super(AttributeNotSetError, self).__init__(message=self.message, skip_print=skip_print)
