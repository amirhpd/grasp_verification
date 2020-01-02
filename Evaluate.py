'''
Evaluate
Plays output.mp4 Video
Receives evaluation of grasped (g) and notgrasped (n) from human
Calculates the accuracy of Inference
Reads output.csv and updates it
Generates dataset suggestions based on mistakes of the learning algorithm
First argument: Save suggestion dataset (0: Don't save, int: interval for frames)
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
import datetime

def main(intervals):
    # text params
    font = cv2.FONT_HERSHEY_PLAIN
    org = (10, 860)
    fontScale = 1.7
    color = (0, 0, 255)
    thickness = 2
    # read csv
    df = pd.read_csv('output.csv')
    df['Actual'] = ''
    # read video
    cap = cv2.VideoCapture('output.mp4')
    fp = cap.get(cv2.CAP_PROP_FPS)
    # start with paused video
    actual = 'N/A'
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=3, fy=3)
    txt = 'Actual: ' + actual + ' - Press "g" or "n".'
    cv2.putText(frame, txt, org, font, fontScale, color, thickness, cv2.LINE_AA)
    while True:
        cv2.imshow('Input', frame)
        c = cv2.waitKey(1)
        if c == 103 :
            actual = 'grasped'
            break
        if c == 110 :
            actual = 'notgrasped'
            break

    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.resize(frame, None, fx=3, fy=3)
            txt = 'Actual: ' + actual
            cv2.putText(frame, txt, org, font, fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('Input', frame)
            c = cv2.waitKey(1)
            if c == 103 : actual = 'grasped'     # 103: g
            if c == 110 : actual = 'notgrasped'  # 110: n
            if i <= len(df)-1:
                df.at[i, 'Actual'] = actual
                i += 1
            time.sleep(1/fp)
            if c == 27: # escape key
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    # compare predict with actual
    df['Compare'] = 0
    for i in df.index:
        if df.loc[i][1] == df.loc[i][2]:
            df.at[i, 'Compare'] = 1
        else:
            for j in range(equalityCoef):
                if df.loc[i-j][1] != df.loc[i-j][2]:
                    df.at[i, 'Compare'] = 0
                else:
                    df.at[i, 'Compare'] = 1
    # calculate accuracy
    accuracy =  round(( (df.agg({'Compare' : ['sum']}).loc['sum'][0] * 100) / len(df) ), 2)
    print('Total Accuracy:', accuracy)
    df['Total Accuracy'] = ''
    df.at[0, 'Total Accuracy'] = accuracy
    # save csv
    df.to_csv('output.csv', index=False)
    # Suggestion dataset
    if intervals != '0':
        if not os.path.exists('suggestions/notgrasped'):
            os.makedirs('suggestions/notgrasped')
        if not os.path.exists('suggestions/grasped'):
            os.makedirs('suggestions/grasped')

        # unique file names
        vidDate = os.path.getmtime('output.mp4')
        dateName = datetime.datetime.utcfromtimestamp(vidDate).strftime("%Y/%m/%d %H:%M:%S").replace(' ', '_').replace('/', ':')
        # crop images
        x = 52; y = 13; h = 215; w = 215

        cap = cv2.VideoCapture('output.mp4')
        fp = cap.get(cv2.CAP_PROP_FPS)
        i = 0
        cnt = 0
        interval = int(intervals)  # if 'interval' frames are wrong, saves one image
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                if i <= len(df)-1:
                    if df.loc[i][3] == 0:
                        cnt += 1
                    else:
                        cnt = 0
                    if cnt == interval:
                        imgCrop = frame[y:y+h, x:x+w]
                        imgCrop = cv2.resize(imgCrop, None, fx=0.595, fy=0.595)
                        name = 'suggestions/' + df.loc[i][2] + '/image_' + dateName + '_' + str(i) + '.jpg'
                        cv2.imwrite(name, imgCrop)
                        cnt = 0
                    i += 1
            else:
                break
    cap.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    equalityCoef = 1      # actual and predict should remain <equalityCoef> frames unequal
    print('Press g if grasped')
    print('Press n if notgrasped')
    print('Press Esc to exit')
    intervals = sys.argv[1]
    main(intervals)
