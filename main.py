from json import dumps
import time
from os import path
import config
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

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
        return self.__session.request(method, urljoin(self.base_url, endpoint), data=dumps(data))

    def create_lobby(self, queueId=450):
        """ 
            queueId 450 is ARAM
            List of valid queue IDs are listed here: https://static.developer.riotgames.com/docs/lol/queues.json
        """
        self.request('post', '/lol-lobby/v2/lobby', {"queueId": queueId})

    def queue(self):
        self.request('post', '/lol-lobby/v2/lobby/matchmaking/search')

    def honor_player(self, playerId=1):
        self.request('post', '/lol-honor-v2/v1/honor-player', {'honorPlayerRequest': playerId})

    def session_phase(self):
        return self.request('get', '/lol-gameflow/v1/session').json().get('phase')

    def accept(self):
        self.request('post', '/lol-matchmaking/v1/ready-check/accept')

    def play_again(self):
        self.request('post', '/lol-lobby/v2/play-again')


if __name__ == '__main__':
    client = LeagueAPI(config.LEAGUE_PATH)
    print("Welcome to ARAM auto-queue.")

    while True:
        phase = client.session_phase()
        # print(f"{phase=}") # debug
        if phase is None:
            client.create_lobby()
        elif phase == 'Lobby':
            client.queue()
        elif phase == 'Matchmaking':
            print("Waiting for queue to pop")
        elif phase == 'ReadyCheck':
            client.accept()
        elif phase in ['ChampSelect', 'InProgress']:
            pass
        elif phase == 'PreEndOfGame':
            client.honor_player()
        elif phase == 'EndOfGame':
            client.play_again()

        # default timeout is 15 seconds
        phase_x_timeout_map = {
            'Lobby': 1,
            'EndOfGame': 1,
            'PreEndOfGame': 1,
        }

        timeout_duration = phase_x_timeout_map.get(phase, 15)
        time.sleep(timeout_duration)

