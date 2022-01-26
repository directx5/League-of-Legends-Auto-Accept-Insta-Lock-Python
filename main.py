from json import dumps
import time
from os import path
import config
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

from requests import Session
from urllib3 import disable_warnings, exceptions

from constants.game_modes import GameModes


class League:
    def __init__(self, league: str):
        with open('champions.txt', 'rb') as file:
            self.champions = {(r := i.split(':'))[0]: r[1] for i in file.read().decode().splitlines()}
        with open(path.join(league, 'lockfile'), 'r', encoding='UTF-8') as lockfile:
            port, self.__password, protocol = lockfile.read().split(':')[2:]
        self.base_url = f'{protocol}://127.0.0.1:{port}/'
        self.__session = Session()
        self.__session.auth = ('riot', self.__password)
        self.__session.verify = False
        disable_warnings(exceptions.InsecureRequestWarning)
        self.summoner = self.request('get', '/lol-summoner/v1/current-summoner').json()

    def request(self, method, endpoint, data=None):
        return self.__session.request(method, urljoin(self.base_url, endpoint), data=dumps(data))

    def is_in_lobby(self):
        return self.request('get', '/lol-lobby/v2/lobby').status_code == 200

    def create_lobby(self, queueType):
        return self.request('post', '/lol-lobby/v2/lobby', {"queueId": 450})

    def queue(self):
        return self.request('post', '/lol-lobby/v2/lobby/matchmaking/search')

    def get_queue_state(self):
        return self.request('get', '/lol-lobby/v2/lobby/matchmaking/search-state').json().get('searchState') 

    def queue_pop(self):
        return self.get_queue_state() == 'Found'

    def is_searching(self):
        return self.get_queue_state() == 'Searching' 

    def accept(self):
        return self.request('post', '/lol-matchmaking/v1/ready-check/accept')

if __name__ == '__main__':
    client = League(config.LEAGUE_PATH)

    if not client.is_in_lobby():
        client.create_lobby(GameModes.ARAM)

    response = client.queue()

    while not client.queue_pop():
        print("Waiting in queue...")
        time.sleep(5)

    client.accept()

