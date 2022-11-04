# README

상태: In progress

# 1. Project Intro

---

- 2022 - 2 Gachon University dept. of software Drone and Robotices Term-Project Team 1
- It is a project about drones that help visually impaired people move

# 2. Tech Stacks

---

- TelloPy [link](https://github.com/hanyazou/TelloPy)
- YOLO v7 ONNX runtime source from this repo : [link](https://github.com/ibaiGorordo/ONNX-YOLOv7-Object-Detection) 
- Python3 

# 3. Functions

---

- Final results can be found inside the TrackingQR.py code.

1. Tracking Human
    - Currently Drone tracking QR code to following human
    - If the QR code goes out of the reference value, tracking is carried out by adjusting the location of the drone and allowing the QR code to fall within the reference value.
2. Detecting obstacle
    - Currently detect car (ex:car,bus,truck...) only 
    - If object detected by drone camera warning sound playing from lap-top
    - In future we're going to increase the number of detectable objects 
    
# 4. run

---
- pre implement : need to download yolov7 onnx model from this [link](https://drive.google.com/file/d/16p4iHgh0sDTxjIzydHFD2YaHAiahs-bw/view)([repo](https://github.com/PINTO0309/PINTO_model_zoo/tree/main/307_YOLOv7)) and add it in model folder.

- command : python trackingQR.py

# 5. Team members

---

1. HAN SooMin -m4a1carbin4(WGNW_gangdodan)
2. LEE JiHo -destiny3912
