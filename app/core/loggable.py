import logging

class Loggable:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)