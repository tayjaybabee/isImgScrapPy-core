""" A package containing custom exceptions for isImgScrapPy """

CHILD_PREFIX = '\nEven more context from caller:\n'

class isImgScrapPyError(Exception):
    p_message = "isImgScrapPyError!\n"

    def __init__(self, message=None, skip_print=False):
        msg_prefix = f"\nSome additional context from the raised exception:\n"
        message = f"{msg_prefix} - {message}" if message is not None else ''

        self.msg_prefix = msg_prefix
        self.message = f"{self.p_message}{self.msg_prefix}- {self.message}"

        if not skip_print:
            print(self.message)



