""" lcu_api.py

Wrapper for league client API
"""

from os import path
from json import dumps
from urllib.parse import urljoin
from requests import Session
from urllib3 import disable_warnings, exceptions


class LeagueAPI:
    def __init__(self, league_path: str):
        with open(path.join(league_path, 'lockfile'), 'r', encoding='UTF-8') as lockfile:
            port, password, protocol = lockfile.read().split(':')[2:]
        self.base_url = f'{protocol}://127.0.0.1:{port}/'
        self.__session = Session()
        self.__session.auth = ('riot', password)
        self.__session.verify = False
        disable_warnings(exceptions.InsecureRequestWarning)

    def request(self, method, endpoint, data=None):
        return self.__session.request(method, urljoin(
            self.base_url, endpoint), data=dumps(data))

    def session_phase(self):
        return self.request(
            'get', '/lol-gameflow/v1/session').json().get('phase')

    def create_lobby(self, queue_id=450):
        """
            queueId 450 is ARAM
            List of valid queue IDs are listed here:
                https://static.developer.riotgames.com/docs/lol/queues.json
        """
        self.request('post', '/lol-lobby/v2/lobby', {"queueId": queue_id})

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
