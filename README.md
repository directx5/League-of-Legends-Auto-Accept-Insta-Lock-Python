# ARAM Auto Queue

This program takes the following actions (depending on game state):

1. Create an ARAM lobby
1. Start queue
1. Wait for champion selection and the game to end...
1. Honor a random player in post-game
1. Hit play again
1. repeat!

_Note: the random player is currently always the second player_

## Requirements

- Python3

## Installation

1. Install [python](https://www.python.org/downloads/)
1. Install dependencies
    `pip install -r requirements.txt`

## Usage

1. Edit `config.py` with your `League of Legends` directory path.
1. Login to league of legends
1. `python3 main.py`

## Reference

- LCU documentation https://lcu.vivide.re/
- LCU utilities https://riot-api-libraries.readthedocs.io/en/latest/lcu.html

## Credits

This project is heavily inspired from [directx's auto-lock script](https://github.com/directx5/League-of-Legends-Auto-Accept-Insta-Lock-Python).