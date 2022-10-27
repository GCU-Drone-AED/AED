import winsound as sound


# Usage
# ww = WarnWorker()
# p = mp.Process(target=ww.run, name="warn")
# p.start()
# p.join()
class WarnWorker:
    def __init__(self):
        self.frequency_range = 2000
        self.duration = 1000

    def run(self):
        sound.Beep(self.frequency_range, self.duration)

