class ValidationError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.messages = msg

class IncompatibleWidget(Exception):
    pass
