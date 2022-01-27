""" main.py

Entrypoint for ARAM-auto-queue

Loads configuration from config.py
Depends on lcu_api.py to interact with league client
"""

import time

from lcu_api import LeagueAPI
import config

def main():
    client = LeagueAPI(config.LEAGUE_PATH)
    print("Welcome to ARAM auto-queue.")

    while True:
        phase = client.session_phase()
        # print(f"{phase=}") # debug
        if phase is None:
            client.create_lobby()
        elif phase == 'Lobby':
            if not config.AUTO_QUEUE:
                continue
            client.queue()
        elif phase == 'Matchmaking':
            pass
        elif phase == 'ReadyCheck':
            client.accept()
        elif phase in ['ChampSelect', 'InProgress']:
            pass
        elif phase == 'PreEndOfGame':
            client.level_change_ack()
            client.reward_granted_ack()
            client.mutual_honor_ack()
            client.honor_player()
        elif phase == 'EndOfGame':
            client.play_again()

        time.sleep(config.POLL_FREQUENCY)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks for using ARAM auto-queue!")
