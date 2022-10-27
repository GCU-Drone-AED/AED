import cv2
import numpy as np
from djitellopy import tello
import multiprocessing as mp

from move_thread import MoveWorker


class TrackingWorker(cv2, np, tello):

    def __init__(self):
        super().__init__()
        self.me = tello.Tello()
        self.me.connect()
        print(self.me.get_battery())

        self.me.streamon()

        # me.takeoff()
        # me.send_rc_control(0 , 0 , 25 , 0)
        # time.sleep(2.2)

        self.width = 640
        self.hight = 480
        self.fbRange = [6200, 6800]
        self.deadZone = 100

        self.pid = [0.4, 0.4, 0]
        self.pError = 0

        self.img = None

    def run(self, img):
        self.img = img
        while True:

            self.img = self.me.get_frame_read().frame
            self.img = self.cv2.resize(self.img, (self.width, self.hight))

            out_img, info = self.findQR(self.img)
            self.pError = self.trackQR(self.me, info, self.width, self.hight, self.pid, self.pError)
            print("Center", info[0], "Area", info[1])
            self.cv2.imshow("Output", out_img)

            if self.cv2.waitKey(1) & 0xFF == ord('q'):
                self.me.land()
                break

    def call_move_process(self, target_drone, speed):
        mw = MoveWorker()
        move_process = mp.Process(target=mw.run, name="AED_move_process", args=(target_drone, speed))
        move_process.start()
        move_process.join()

    def findQR(self, img):
        det = self.cv2.QRCodeDetector()
        imgGray = self.cv2.cvtColor(img, self.cv2.COLOR_RGB2GRAY)
        _, box_coordinates = det.detect(img)

        QR_C = []
        QR_Area = []

        x, y = None
        if box_coordinates is not None:

            box_coordinates = [box_coordinates[0].astype(int)]
            nrOfbox_coordinates = len(box_coordinates[0])
            print(box_coordinates)

            for i in range(nrOfbox_coordinates):

                control = i % nrOfbox_coordinates

                print(control)

                if (control == 0):
                    x, y = tuple(box_coordinates[0][control])

                    print(x, y)
                elif (control == 2):
                    x1, y1 = tuple(box_coordinates[0][control])
                    w = x1 - x
                    h = y1 - y

                    self.cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cx = x + w // 2
                    cy = y + h // 2
                    area = w * h

                    print(cx, cy)

                    self.cv2.circle(img, (cx, cy), 5, (0, 255, 0), self.cv2.FILLED)

                    QR_C.append([cx, cy])
                    QR_Area.append(area)

        else:
            return img, [[0, 0], 0]

        if len(QR_Area) != 0:
            i = QR_Area.index(max(QR_Area))
            print("return value")
            return img, [QR_C[i], QR_Area[i]]
        else:
            return img, [[0, 0], 0]

    def trackQR(self, me, info, w, h, pid, pError):
        area = info[1]
        x, y = info[0][0], info[0][1]
        fb = 0
        ud = 0

        error = x - w // 2
        speed = pid[0] * error + pid[1] * (error - pError)
        speed = int(np.clip(speed, -100, 100))

        if area > self.fbRange[0] and area < self.fbRange[1]:
            fb = 0
        elif area > self.fbRange[1]:
            fb = -20
        elif area < self.fbRange[0] and area != 0:
            fb = 20

        if (y > int(h * 2 / 3) + self.deadZone):
            ud = -20
        elif (y < int(h * 2 / 3) - self.deadZone):
            ud = +20

        if x == 0:
            speed = 0
            error = 0

        me.send_rc_control(0, fb, ud, speed)
        return error

"""me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()

#me.takeoff()
#me.send_rc_control(0 , 0 , 25 , 0)
# time.sleep(2.2)

width = 640
hight = 480
fbRange = [6200, 6800]
deadZone = 100

pid = [0.4, 0.4, 0]
pError = 0"""






