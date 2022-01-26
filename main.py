""" main.py

Entrypoint for ARAM-auto-queue

Loads configuration from config.py
Depends on lcu_api.py to interact with league client
"""

import time

from lcu_api import LeagueAPI
import config

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
            pass
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
            None: 1,
            'Lobby': 1,
            'EndOfGame': 1,
            'PreEndOfGame': 1,
        }

        timeout_duration = phase_x_timeout_map.get(phase, 15)
        time.sleep(timeout_duration)
