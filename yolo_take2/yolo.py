import cv2
import argparse
import numpy as np
import api

from picamera import PiCamera
from time import sleep, time

# args
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=False,
                help = 'path to input image')
ap.add_argument('-c', '--config', required=True,
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help = 'path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help = 'path to text file containing class names')
args = ap.parse_args()

#SETUP

#loadClasses = "~/Desktop/detection/yolo_take2/yolov3.txt"
#config = "~/Desktop/detection/yolo_take2/yolov3.cfg"
#weights = "~/Desktop/detection/yolo_take2/yolov3.weights"

# take image
camera = PiCamera()
camera.capture('cap.jpg')

image = cv2.imread('cap.jpg')

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

# can crop images yay
#image = image[round((Height - 100)/2):Height, 0:Width]

# bounds for spot id calculation if only looking at 3 spots
# would need 4th bound if looking at 4 spots
bound1 = 1500
bound2 = 2800

# read class names
classes = None
with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# read the pre-trained model and config file
net = cv2.dnn.readNet(args.weights, args.config)

# create an input blob
blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0,0,0), True, crop=False)

# set the input blob for the net
net.setInput(blob)

#ENDSETUP

# function to get the output layer names
def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

# function to draw bounding boxes
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    cv2.rectangle(img, (int(x),int(y)), (int(x_plus_w), int(y_plus_h)), (0, 255, 0), 2)
    cv2.putText(img, label, (int(x)-10, int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


def detect():
    #READY TO ACTUALLY DO SOMETHING
    outs = net.forward(get_output_layers(net))

    # init
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    spot1 = 0
    spot2 = 0
    spot3 = 0

    # for each detection from each output layer
    # get the conf, class id, bounding boxes
    # ignore weak detections (conf < 0.5)
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.6:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    #WE DID SOMETHING
    #WE DID TO MUCH
    #AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

    # apply nms
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # go through the detections remaining after nms and draw some boxes yeaaaaa
    count = 0
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

        center = ((x+x+w)/2, (y +y+h)/2)
        #cv2.line(image, (round(center[0]), 5000), (round(center[0]), 0), (0, 255, 0), 2)

        if str(classes[class_ids[i]]) == "car" or str(classes[class_ids[i]]) == "truck":
            if 0 < center[0] < bound1:
                spot1 = 1
            elif bound1 < center[0] < bound2:
                spot2 = 1
            elif bound2 < center[0] < Width:
                spot3 = 1

        # print(center)
        #
        # print("----------------")
        # print(x)
        # print(y)
        # print(w)
        # print(h)
        # print("----------------")

        if str(classes[class_ids[i]]) == "car" or str(classes[class_ids[i]]) == "truck":
            count = count + 1

        draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

    #cv2.line(image, (1000, 5000), (1000, 0), (0, 255, 0), 2)
    #cv2.line(image, (2000, 5000), (2000, 0), (0, 255, 0), 2)

    # save the result image
    cv2.imwrite("~/Desktop/detection/yolo_take2/result.jpg", image)

    res = api.update_sensor("1C", {'garage': "C", 'cars': count, 'lastUpdated': time(), 'spots': [{
                                                                            'spotID': 1, 'occupied': spot1
                                                                            },
                                                                            {
                                                                            'spotID': 2, 'occupied': spot2
                                                                            },
                                                                            {
                                                                            'spotID': 3, 'occupied': spot3
                                                                            }
                                                                        ]});

if __name__ == "__main__":
    #while(1):
    detect()
    #    sleep(1)
