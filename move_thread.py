from djitellopy import Tello
import time


# Usage
# mw = MoveWorker()
# p = mp.Process(target=mw.run, name="move", args=(target_drone, speed))
# p.start()
# p.join()
class MoveWorker:
    def __init__(self):
        self.target_drone = None
        self.speed = None

    def run(self, target_drone, speed):
        self.target_drone = target_drone
        self.speed = speed

        self.target_drone.go_xyz_speed(1, 0, 0, self.speed)
        print("move forward")
        time.sleep(10)
