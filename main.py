from json import dumps
from os import path
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

from requests import Session
from urllib3 import disable_warnings, exceptions


class League:
    def __init__(self, league: str):
        with open('champions.txt', 'r', encoding='UTF-8') as file:
            c = [i.split(':') for i in file.read().splitlines()]
            self.champions = dict(zip([i[0] for i in c], [i[1] for i in c]))
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

    def is_found(self):
        return self.request('get', '/lol-lobby/v2/lobby/matchmaking/search-state').json().get('searchState') == 'Found'

    def is_searching(self):
        value = self.request('get', '/lol-lobby/v2/lobby/matchmaking/search-state').json().get('searchState')
        return value == 'Searching'

    def is_selecting(self):
        return self.request('get', '/lol-champ-select/v1/session').json().get('actions')

    def is_playing(self):
        return self.request('get', '/lol-gameflow/v1/session').json()['gameClient'].get('running')

    def accept(self):
        self.request('post', '/lol-matchmaking/v1/ready-check/accept')

    def select_champion(self, champion_name: str, qid: int):
        data = {"championId": self.champions.get(champion_name), 'completed': True}
        self.request('patch', f'/lol-champ-select/v1/session/actions/{qid}', data)

    def is_me(self, qid: int):
        return self.request('get', f'/lol-champ-select/v1/summoners/{qid}').json().get('isSelf')

    def select(self, champion: str):
        with ThreadPoolExecutor() as executor:
            me = 5 if len(x := [i for i in range(0, 5) if executor.submit(self.is_me, i).result()]) == 0 else x[0]
            self.select_champion(champion, me)

    def chat(self, lane: str):
        data = {'body': lane}
        while True:
            try:
                chat_id = self.request('get', '/lol-chat/v1/conversations').json()[0]['id']

                def sent_by(sid: int, cnt: str):
                    messages = self.request('get', f'/lol-chat/v1/conversations/{chat_id}/messages').json()
                    if any(x.get('fromSummonerId') == sid and cnt in x.get('body') for x in messages):
                        return True
                    else:
                        return False

                def everyone_in_lobby():
                    session = self.request('get', '/lol-champ-select/v1/session').json()
                    messages = self.request('get', f'/lol-chat/v1/conversations/{chat_id}/messages').json()
                    team_players = [x for x in session['actions'][0] if x['isAllyAction']]
                    return len(team_players) <= len(messages)

                if everyone_in_lobby() and not sent_by(self.summoner['summonerId'], lane):
                    self.request('post', f'/lol-chat/v1/conversations/{chat_id}/messages', data=data)
                    break
                else:
                    continue
            except IndexError:
                continue
            except KeyError:
                break


if __name__ == '__main__':
    client = League('League Path')
    while not client.is_playing():
        if client.is_selecting():
            client.select('Champion')
            client.chat('Lane')
        elif client.is_found():
            client.accept()
        else:
            continue
