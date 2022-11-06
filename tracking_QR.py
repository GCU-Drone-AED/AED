#import list
import cv2
import numpy as np
from djitellopy import tello
from YOLOv7 import YOLOv7
import time
import beepy as beep

#image data
width = 640 
hight = 480

#tracking QR Area
fbRange = [6200, 6800]
deadZone = 40

#user danger_area data
detect_width = 250
detect_hight = 180

#tracking QR PID 
pid = [0.1, 0.1, 0]
pError = 0

# danger_object index
danger_item = [1, 2, 3, 5, 7]
count = 0

# class for detecting object and check collision
class detect_warn:

    def __init__(self):
        self.frequency_range = 2000
        self.duration = 1000
        # Initialize YOLOv7 object detector
        self.model_path = "models/yolov7-tiny_480x640.onnx"
        #self.model_path = "models/yolov7_480x640.onnx"
        self.yolov7_detector = YOLOv7(
            self.model_path, conf_thres=0.3, iou_thres=0.5)

    # collision detect and sound_warning 
    def sound_warning(self, obj, user_position):
        count = 0 

        ux0, uy0, ux1, uy1 = user_position

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

            if (count != 0):
                print("danger!\n")
                beep.beep(sound=1)
            else : 
                print("safe\n")
            return 

    #check Image and start object detection
    def run(self, img, user_position):

        cv2.namedWindow("Detected Objects", cv2.WINDOW_NORMAL)

        boxes, scores, class_ids = self.yolov7_detector(img)

        danger_obj = []

        for i, value in enumerate(class_ids):
            if (value in danger_item):
                danger_obj.append(boxes[i])

        self.sound_warning(danger_obj, user_position)

        # Draw detections -> not that important
        combined_img = self.yolov7_detector.draw_detections(img)
        cv2.imshow("Detected Objects", combined_img)

#find QR(user) and return QR data (position, Area)
def findQR(img):
    #detect QR
    det = cv2.QRCodeDetector()
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    #get detect data.
    _, box_coordinates = det.detect(img)

    QR_C = []
    QR_Area = []

    if box_coordinates is not None:

        box_coordinates = [box_coordinates[0].astype(int)]
        nrOfbox_coordinates = len(box_coordinates[0])

        # find center x,y and w,h 
        for i in range(nrOfbox_coordinates):

            control = i % nrOfbox_coordinates 
            
            if(control == 0):
                x, y = tuple(box_coordinates[0][control])
            elif(control == 2):
                x1, y1 = tuple(box_coordinates[0][control])
                w = x1 - x
                h = y1 - y
                
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cx = x + w // 2
                cy = y + h // 2
                area = w * h

                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

                QR_C.append([cx, cy])
                QR_Area.append(area)

    else:
        return img, [[0, 0], 0]

    if len(QR_Area) != 0:
        i = QR_Area.index(max(QR_Area))
        return img, [QR_C[i], QR_Area[i]]
    else:
        return img, [[0, 0], 0]

#Drone tracking QR
def trackQR(me, info, w, h, pid, pError):
    #set QR data
    area = info[1]
    x,y = info[0][0],info[0][1]
    fb = 0
    ud = 0

    error = x - w//2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    #move foward check
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    #up down check
    if (y > int(h*3/4) + deadZone):
        ud = -5
    elif(y < int(h*3/4) - deadZone):
        ud = +5

    if x == 0:
        speed = 0
        error = 0

    #send drone_command to tracking QR(USER)
    me.send_rc_control(0, fb, ud, speed)
    return error

if __name__ == '__main__':
    #class init
    detect_object = detect_warn()

    #tello drone init
    me = tello.Tello()
    me.connect()
    print(me.get_battery())

    me.streamon()

    me.takeoff()
    me.send_rc_control(0 , 0 , 25 , 0)
    time.sleep(2.2)

    # keep read IMG from tello drone and tracking QR + Obejct detection
    while True:
        time.sleep(0.05)
        img = me.get_frame_read().frame
        img = cv2.resize(img, (width, hight))

        img0, info = findQR(img)

        cx,cy = info[0][0],info[0][1]

        ux0,uy0,ux1,uy1 = int(np.clip(cx - detect_width/2,0,680)),int(np.clip(cy - detect_hight,0,480)),int(np.clip(cx + detect_width/2,0,680)),int(np.clip(cy,0,480))

        user_position = [ux0,uy0,ux1,uy1]

        detect_object.run(img,user_position)

        pError = trackQR(me, info, width, hight, pid, pError)
        print("Center",info[0],"Area",info[1])
        cv2.imshow("Output", img0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            me.land()
            break

    cv2.destroyAllWindows()
