from json import dumps
import time
from os import path
import config
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

from requests import Session
from urllib3 import disable_warnings, exceptions

from constants.game_modes import GameModes


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
        return self.__session.request(method, urljoin(self.base_url, endpoint), data=dumps(data))

    def create_lobby(self, queueId=450):
        """ 
            queueId 450 is ARAM
            List of valid queue IDs are listed here: https://static.developer.riotgames.com/docs/lol/queues.json
        """
        self.request('post', '/lol-lobby/v2/lobby', {"queueId": queueId})

    def queue(self):
        self.request('post', '/lol-lobby/v2/lobby/matchmaking/search')

    def session_phase(self):
        return self.request('get', '/lol-gameflow/v1/session').json().get('phase')

    def accept(self):
        self.request('post', '/lol-matchmaking/v1/ready-check/accept')

if __name__ == '__main__':
    client = LeagueAPI(config.LEAGUE_PATH)
    print("Welcome to ARAM auto-queue.")

    while True:
        timeout = 5 # default polling period is 5 seconds

        phase = client.session_phase()
        if phase is None:
            client.create_lobby()
        elif phase == 'Lobby':
            client.queue()
        elif phase == 'Matchmaking':
            print("Waiting for queue to pop")
        elif phase == 'ReadyCheck':
            client.accept()
        elif phase in ['ChampSelect', 'InProgress', 'PreEndOfGame']:
            # Waiting for game to complete, check once every 15 seconds
            timeout = 15
        elif phase == 'EndOfGame':
            print("TODO: create lobby?")

        time.sleep(timeout)

