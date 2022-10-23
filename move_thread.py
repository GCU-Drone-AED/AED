import threading
from djitellopy import Tello
import time


class MoveWorker(threading.Thread):
    def __init__(self, target_drone, speed):
        super().__init__()
        self.target_drone = target_drone
        self.speed = speed

    def run(self):
        target_drone = self.target_drone
        speed = self.speed

        target_drone.go_xyz_speed(1, 0, 0, speed)
        time.sleep(10)
