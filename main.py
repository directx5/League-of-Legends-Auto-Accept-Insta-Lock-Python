""" main.py

Entrypoint for ARAM-auto-queue

"""

import multiprocessing
import PySimpleGUI as sg
from config import Config
from lcu_api import LeagueAPI


def launch_gui(league_api):
    sg.theme('DefaultNoMoreNagging')
    layout = [
        [sg.Text('Not running', key='status')],
        [sg.Checkbox(
            'Auto start queue',
            key='AUTO_QUEUE',
            default=cfg.AUTO_QUEUE,
            enable_events=True
        )],
        [sg.Button('Start', key='toggle')],
    ]

    window = sg.Window(
        title="ARAM auto-queue",
        layout=layout,
    )

    # Run lcu_api in the background, store its process in MAIN_PROC
    background_proc = None

    # GUI event loop handler
    while True:
        event, _ = window.read()

        if event == 'toggle':
            background_proc = toggle_process(background_proc, league_api)
            window['status'].update('Running' if background_proc else 'Not running')
            window['toggle'].update('Stop' if background_proc else 'Start')
            window['AUTO_QUEUE'].update(disabled=bool(background_proc))

        elif event == 'AUTO_QUEUE':
            cfg.AUTO_QUEUE = not cfg.AUTO_QUEUE
            league_api.update_config(cfg)
            window['AUTO_QUEUE'].update(cfg.AUTO_QUEUE)

        elif event == sg.WINDOW_CLOSED:
            if background_proc:
                background_proc.terminate()
            break


def toggle_process(proc, league_api):
    if proc is not None:
        proc.terminate()
        return None

    proc = multiprocessing.Process(target=league_api.loop, args=())
    proc.start()
    return proc


if __name__ == '__main__':
    cfg = Config()
    launch_gui(LeagueAPI(cfg))
