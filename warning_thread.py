import threading
import time
import winsound as sound


def warning():
    frequency_range = 2000
    duration = 1000

    sound.Beep(frequency_range, duration)


class MoveWorker(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        warning()

