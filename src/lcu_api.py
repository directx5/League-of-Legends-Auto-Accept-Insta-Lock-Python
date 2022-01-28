""" lcu_api.py

Wrapper for league client API
"""

from json import dumps
from urllib.parse import urljoin
import time
from requests import Session
from urllib3 import disable_warnings, exceptions
from proc_utils import lcu_process_args
from config import Config
from constants import QueueType


class LeagueAPI:
    def __init__(self, config: Config):
        self.config = config
        process_args = lcu_process_args()
        self.base_url = f'https://127.0.0.1:{process_args["app-port"]}/'
        self.__session = Session()
        self.__session.auth = ('riot', process_args['remoting-auth-token'])
        self.__session.verify = False  # LCU api uses a self-signed cert

    def loop(self):
        disable_warnings(exceptions.InsecureRequestWarning)
        while True:
            self.run()
            sleep_duration = 1
            time.sleep(sleep_duration)

    def run(self):
        phase = self.session_phase()
        if phase is None:
            if self.config.AUTO_LOBBY:
                self.create_lobby(self.config.QUEUE_ID)
        elif phase == 'Lobby':
            if self.config.AUTO_QUEUE:
                self.queue()
        elif phase == 'Matchmaking':
            pass
        elif phase == 'ReadyCheck':
            if self.config.AUTO_ACCEPT:
                self.accept()
        elif phase in ['ChampSelect', 'InProgress']:
            pass
        elif phase == 'PreEndOfGame':
            if self.config.AUTO_SKIP_POSTGAME:
                self.level_change_ack()
                self.reward_granted_ack()
                self.mutual_honor_ack()
                self.honor_player()
        elif phase == 'EndOfGame':
            if self.config.AUTO_PLAY_AGAIN:
                self.play_again()

    def update_config(self, config):
        self.config = config

    def request(self, method, endpoint, data=None):
        return self.__session.request(method, urljoin(
            self.base_url, endpoint), data=dumps(data))

    def session_phase(self):
        return self.request(
            'get', '/lol-gameflow/v1/session').json().get('phase')

    def create_lobby(self, queue_type: QueueType):
        """
            queueId 450 is ARAM
            List of valid queue IDs are listed here:
                https://static.developer.riotgames.com/docs/lol/queues.json
        """
        self.request('post', '/lol-lobby/v2/lobby', {"queueId": queue_type.value})

    def queue(self):
        self.request('post', '/lol-lobby/v2/lobby/matchmaking/search')

    def accept(self):
        self.request('post', '/lol-matchmaking/v1/ready-check/accept')

    def honor_player(self, player_id=1):
        self.request('post', '/lol-honor-v2/v1/honor-player',
                     {'honorPlayerRequest': player_id})

    def level_change_ack(self):
        self.request('post', '/lol-honor-v2/v1/level-change/ack')

    def reward_granted_ack(self):
        self.request('post', '/lol-honor-v2/v1/reward-granted/ack')

    def mutual_honor_ack(self):
        self.request('post', '/lol-honor-v2/v1/mutual-honor/ack')

    def play_again(self):
        self.request('post', '/lol-lobby/v2/play-again')
