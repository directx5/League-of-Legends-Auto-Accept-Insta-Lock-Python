# ARAM Auto Queue ![lint](https://github.com/SaffatHasan/Aram-Auto-Queue/actions/workflows/pylint.yml/badge.svg)

This program takes the following actions:

1. Create an ARAM lobby
1. Start queue
1. Wait for champion selection and the game to end...
1. Honor a random player in post-game
1. Hit play again
1. Repeat!

## Requirements

- Python3

## Installation

1. Install [python](https://www.python.org/downloads/)
1. Install dependencies
    `pip install -r requirements.txt`

## Usage

1. Login to league of legends
1. `python3 main.py`

## Configuration

Some useful options are listed in `config.py`. Current configuration items are:

* `AUTO_QUEUE`: Clicks "FIND MATCH" for you

## Reference

- LCU documentation https://lcu.vivide.re/
- LCU utilities https://riot-api-libraries.readthedocs.io/en/latest/lcu.html

## Credits

This project is heavily inspired from [directx's auto-lock script](https://github.com/directx5/League-of-Legends-Auto-Accept-Insta-Lock-Python).
