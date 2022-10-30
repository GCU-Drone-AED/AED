import multiprocessing as mp
import cv2
from move_thread import MoveWorker
from warning_thread import WarnWorker
from tracking_QR import TrackingWorker


def call_warn_process():
    ww = WarnWorker()
    warn_process = mp.Process(target=ww.run, name="AED_warn_process")
    warn_process.start()
    warn_process.join()


def call_tracking_process(img):
    tw = TrackingWorker()
    tracking_process = mp.Process(target=tw.run, name="AED_tracking_process", args=(img,))
    tracking_process.start()
    tracking_process.join()


if __name__ == "__main__":
    print("do something")
    cap = cv2.VideoCapture(0)
    _, img = cap.read()