""" config.py
"""

# pylint: disable=C0103, R0903
from constants import QueueType

class Config:
    def __init__(self):
        self.AUTO_LOBBY = True
        self.QUEUE_ID = QueueType.RANKED
        self.AUTO_QUEUE = True
        self.AUTO_ACCEPT = True
        self.AUTO_SKIP_POSTGAME = True
        self.AUTO_PLAY_AGAIN = True
