import os
from time import sleep

while(1):
    #os.system("python3 sensor1.py & python3 sensor2.py & python3 sensor3.py")
    os.system("python ~/Desktop/detection/yolo_take2/yolo.py -c ~/Desktop/detection/yolo_take2/yolov3.cfg -w ~/Desktop/detection/yolo_take2/yolov3.weights -cl ~/Desktop/detection/yolo_take2/yolov3.txt")
    sleep(10)
