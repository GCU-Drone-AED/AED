import cv2
import numpy as np
from djitellopy import tello

me = tello.Tello()
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
pError = 0

def findQR(img):
    det = cv2.QRCodeDetector()
    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, box_coordinates = det.detect(img)

    QR_C = []
    QR_Area = []

    if box_coordinates is not None:

        box_coordinates = [box_coordinates[0].astype(int)]
        nrOfbox_coordinates = len(box_coordinates[0])
        print (box_coordinates)

        for i in range(nrOfbox_coordinates):

            control = i % nrOfbox_coordinates 

            print(control)
            
            if(control == 0):
                x, y = tuple(box_coordinates[0][control])

                print(x,y)
            elif(control == 2):
                x1, y1 = tuple(box_coordinates[0][control])
                w = x1 - x
                h = y1 - y
                
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cx = x + w // 2
                cy = y + h // 2
                area = w * h

                print(cx,cy)

                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

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


def trackQR(me, info, w, h, pid, pError):
    area = info[1]
    x,y = info[0][0],info[0][1]
    fb = 0
    ud = 0

    error = x - w//2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if (y > int(h*2/3) + deadZone):
        ud = -20
    elif(y < int(h*2/3) - deadZone):
        ud = +20

    if x == 0:
        speed = 0
        error = 0

    me.send_rc_control(0, fb, ud, speed)
    return error


cap = cv2.VideoCapture(0)
while True:
    #_, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (width, hight))

    img, info = findQR(img)
    pError = trackQR(me, info, width, hight, pid, pError)
    print("Center",info[0],"Area",info[1])
    cv2.imshow("Output", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
