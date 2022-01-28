""" config.py
"""

# pylint: disable=C0103, R0903


class Config:
    def __init__(self):
        self.AUTO_QUEUE = False
        self.AUTO_LOBBY = True
        self.AUTO_ACCEPT = True
        self.AUTO_SKIP_POSTGAME = True
        self.AUTO_PLAY_AGAIN = True
