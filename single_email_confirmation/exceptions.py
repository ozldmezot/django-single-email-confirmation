class ConfirmationTokenDoesNotExistException(Exception):
    def __init__(self, value):
        self.token = value
    def __str__(self):
        return repr(self.token)