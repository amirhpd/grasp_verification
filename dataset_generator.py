'''
Dataset generator
Reads camera no.1, saves 128x128 images
First argument: Class (folder) name
Second argument: frames interval
Software License Agreement (MIT License)
Copyright (c) 2020, Amirhossein Pakdaman.
'''
import cv2
import os
import sys

def main(className, captureRate):
    # create dir & get current file No.
    if not os.path.exists(className):
        os.makedirs(className)
    fileNo = 1
    while (True):
        fileName = className + '/image_' + str(fileNo) + '.jpg'
        if os.path.isfile(fileName):
            fileNo += 1
        else: break

    # start camera
    cap = cv2.VideoCapture(1)
    # inference: 320*308 , dataset collection: 256*256
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open camera")

    cnt0 = 0
    capture = False
    while True:
        # capture
        if capture == True:
            ret, frame = cap.read()
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
            if cnt0 == captureRate:
                name = className + '/image_' + str(fileNo) + '.jpg'
                cv2.imwrite(name, frame)
                fileNo += 1
                cnt0 = 0
            cnt0 += 1
        # display
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=3, fy=3)
        cv2.imshow('Input', frame)
        # read keys
        c = cv2.waitKey(1)
        if c == 32: # space key
            capture = not capture
            print('capture: ', capture)
        if c == 27: # escape key
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    className = sys.argv[1]
    captureRate = int(sys.argv[2])
    main(className, captureRate)
