import os
from time import sleep

while(1):
    #os.system("python3 sensor1.py & python3 sensor2.py & python3 sensor3.py")
    #os.system("python3 thresh1.py & python3 thresh2.py & python3 thresh3.py")
    #os.system("python3 bat1.py & python3 bat2.py & python3 bat3.py")
    #os.system("python3 id1.py & python3 id2.py & python3 id3.py")
    os.system("python ~/Desktop/detection/yolo_take2/yolo.py -c ~/Desktop/detection/yolo_take2/yolov3.cfg -w ~/Desktop/detection/yolo_take2/yolov3.weights -cl ~/Desktop/detection/yolo_take2/yolov3.txt")
    sleep(10)
