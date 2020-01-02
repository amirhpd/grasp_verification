'''
Inference
Runs TensorflowEasy module of JeVois camera
Displays the camera output
Reads the classification results from USB
Saves the output video as .mp4 file
Saves classification results as .csv file
First argument: Save video and csv files (0/1)
Software License Agreement (MIT License)
Copyright (c) 2020, Amirhossein Pakdaman.
'''
import sys
import numpy as np
import cv2
import os
import serial
import time
import pandas as pd

def main(saveFiles):
    df = pd.DataFrame(columns=['Time', 'Predict'])
    # set serial
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)
    except Exception as e:
        try:
            ser = serial.Serial('/dev/ttyACM1', 115200, timeout=0.01)
        except Exception as e:
            raise IOError('No camera')
    time.sleep(0.5)
    ser.write(('setpar serout USB' + '\n').encode())
    # set camera
    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 308)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # getting fps
    for i in range(2):
        ret,frame = cap.read() # increases the accuracy of fps calculation

    s = cv2.getTickCount()
    ret,frame = cap.read()
    fp = cv2.getTickFrequency() / (cv2.getTickCount() - s)
    # print('fps:', fp)
    # save video
    if saveFiles == '1':
        out = cv2.VideoWriter('output.mp4', fourcc, fp, (320,308))
    tm1 = time.time()
    # check camera
    if not cap.isOpened():
        raise IOError("Cannot open camera")

    print('Press Esc to exit')
    i = 0
    while True:
        ret, frame = cap.read()
        if saveFiles == '1': out.write(frame)
        frame = cv2.resize(frame, None, fx=3, fy=3)
        cv2.imshow('Input', frame)

        # read serial
        tm2 = round(time.time()-tm1, 2)
        line = ser.readline().rstrip()
        if str(line).split()[0] == "b'TO":
            df.loc[i] = [tm2, str(line).split()[1].split(':')[0][:-1]]
            i += 1
        c = cv2.waitKey(1)
        if c == 27: # escape key
            break

    cap.release()
    if saveFiles == '1': out.release()
    cv2.destroyAllWindows()
    if saveFiles == '1':
        df.to_csv('output.csv', index=False)



if __name__ == "__main__":
    print('Initializing ...')
    saveFiles = sys.argv[1]
    main(saveFiles)
