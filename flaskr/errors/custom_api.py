class CustomAPIError(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv