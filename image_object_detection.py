from multiprocessing.sharedctypes import Value
import cv2
import numpy as np
from djitellopy import tello
import time

from YOLOv7 import YOLOv7

# Initialize YOLOv7 object detector
model_path = "models/yolov7-tiny_480x640.onnx"
#model_path = "models/yolov7_480x640.onnx"
yolov7_detector = YOLOv7(model_path, conf_thres=0.3, iou_thres=0.5)


danger_item = [1, 2, 3, 5, 7]
"""me = tello.Tello()
me.connect()
print(me.get_battery())

me.streamon()"""

cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)


def sound_warning(obj):

    count = 0

    ux0, uy0, ux1, uy1 = 355, 7, 530, 107

    num = len(obj)

    if num == 0:
        return 
    else:
        for tmp in obj:
            x0, y0, x1, y1 = tmp

            print(x0,y0,x1,y1)

            if (x1 < ux0 or x0 > ux1):
                continue
            if (y1 < uy0 or y0 > uy1):
                continue
            count += 1
            break

        print(count)
        if (count != 0):
            print("danger!\n")
        return 

count = 0

while True:
    # Detect Objects
    #img = me.get_frame_read().frame
    img = cv2.imread("test.jpeg")
    boxes, scores, class_ids = yolov7_detector(img)

    danger_obj = []

    for i, value in enumerate(class_ids):
        if (value in danger_item):
            danger_obj.append(boxes[i])

    sound_warning(danger_obj)

    # Draw detections
    combined_img = yolov7_detector.draw_detections(img)
    cv2.imshow("Detected Objects", combined_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # me.land()
        break

cv2.destroyAllWindows()
