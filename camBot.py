'''
camBot
Reads robot's status, reads camera's inference results,
evaluates real-world accuracy, updates scv file,
generates and saves suggestion images.
Software License Agreement (MIT License)
Copyright (c) 2020, Amirhossein Pakdaman.
'''
#!/usr/bin/python 
import numpy as np
import cv2
import os
import serial
import time
import pandas as pd
import datetime
import sys

def readRobot():
    file = open('conn.txt','r')
    file.seek(0)
    conn = file.read(3)
    conn = list(conn)
    conn = [int(c) for c in conn]
    robotRun, robotArm, robotGripper = 'N/A', 'N/A', 'N/A'
    if conn[0] == 0 : robotRun = 'stop'
    if conn[0] == 1 : robotRun = 'running'
    if conn[1] == 0 : robotArm = 'up'
    if conn[1] == 1 : robotArm = 'down'
    if conn[2] == 0 : robotGripper = 'open'
    if conn[2] == 1 : robotGripper = 'close'
    return robotRun, robotArm, robotGripper

def getAccuracy(df, equalityCoef):
    df['Compare'] = 0
    for i in df.index:
        if (df.loc[i][1] == 'grasped') and (df.loc[i][4] == 'close') or (df.loc[i][1] == 'notgrasped') and (df.loc[i][4] == 'open'):
            df.at[i, 'Compare'] = 1
        else:
            if i > equalityCoef :
                for j in range(equalityCoef):
                    if (df.loc[i-j][1] != 'grasped') or (df.loc[i-j][4] != 'close'):
                        df.at[i, 'Compare'] = 0
                    else:
                        df.at[i, 'Compare'] = 1
            else:
                df.at[i, 'Compare'] = 0

    accuracy = (df.agg({'Compare' : ['sum']}).loc['sum'][0] * 100) / len(df)
    accuracy = round(accuracy, 2)
    acc = 'accuracy: ' + str(accuracy) + ' %'
    print(acc)
    df['Total Accuracy'] = ''
    df.at[0, 'Total Accuracy'] = accuracy

def genSuggestion(df, dirName, interval):
    if not os.path.exists(dirName+'/suggestions/notgrasped'):
        os.makedirs(dirName+'/suggestions/notgrasped')
    if not os.path.exists(dirName+'/suggestions/grasped'):
        os.makedirs(dirName+'/suggestions/grasped')

    x = 52; y = 13; h = 215; w = 215

    vidDate = os.path.getmtime(dirName+'/output.mp4')
    dateName = datetime.datetime.utcfromtimestamp(vidDate).strftime(
                "%Y/%m/%d %H:%M:%S").replace(' ', '_').replace('/', ':')

    cap = cv2.VideoCapture(dirName+'/output.mp4')
    fp = cap.get(cv2.CAP_PROP_FPS)
    i = 0
    cnt = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if i <= len(df)-1:
                if df.loc[i][5] == 0:
                    cnt += 1
                else:
                    cnt = 0
                if cnt == interval:
                    if df.loc[i][4] == 'close' : className = 'grasped'
                    if df.loc[i][4] == 'open' : className = 'notgrasped'
                    imgCrop = frame[y:y+h, x:x+w]
                    imgCrop = cv2.resize(imgCrop, None, fx=0.595, fy=0.595)
                    name = dirName + '/suggestions/' + className + '/image_' + dateName + '_' + str(i) + '.jpg'
                    cv2.imwrite(name, imgCrop)
                    cnt = 0
                i += 1
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

def checkRequirments():
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)
    except Exception as e:
        try:
            ser = serial.Serial('/dev/ttyACM1', 115200, timeout=0.01)
        except Exception as e:
            raise IOError('No camera')

    cap = cv2.VideoCapture(cameraInput)
    if not cap.isOpened():
        raise IOError("Cannot open camera")

    if not os.path.exists('conn.txt'):
        f1 = open('conn.txt','w')
        f1.write('000')
        f1.close()


def main(dirName):
    df = pd.DataFrame(columns=['Time', 'Predict', 'Robot', 'Arm', 'Gripper'])
    font = cv2.FONT_HERSHEY_PLAIN

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

    cap = cv2.VideoCapture(cameraInput)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 308)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')

    for i in range(2):
        ret,frame = cap.read()

    s = cv2.getTickCount()
    ret,frame = cap.read()
    fp = cv2.getTickFrequency() / (cv2.getTickCount() - s)
    print('fps:', fp)

    out = cv2.VideoWriter(dirName+'/output.mp4', fourcc, fp, (320,308))
    tm1 = time.time()

    if not cap.isOpened():
        raise IOError("Cannot open camera")

    i = 0
    while True:
        robotRun, robotArm, robotGripper = readRobot()
        ret, frame = cap.read()
        txt1 = 'Robot :   ' + robotRun
        txt2 = 'Arm :     ' + robotArm
        txt3 = 'Gripper : ' + robotGripper
        cv2.putText(frame, txt1, (6, 278), font, 0.9, (0, 0, 255), 1, cv2.LINE_8)
        cv2.putText(frame, txt2, (6, 290), font, 0.9, (0, 0, 255), 1, cv2.LINE_8)
        cv2.putText(frame, txt3, (6, 302), font, 0.9, (0, 0, 255), 1, cv2.LINE_8)
        out.write(frame)
        frame = cv2.resize(frame, None, fx=3, fy=3)
        cv2.namedWindow('JeVois_view')
        cv2.moveWindow('JeVois_view', 40,30)
        cv2.imshow('JeVois_view', frame)

        # read serial
        tm2 = round(time.time()-tm1, 2)
        line = ser.readline().rstrip()
        if str(line).split()[0] == "TO":
            # df.loc[i] = [tm2, str(line).split()[1].split(':')[0][:-1], robotRun, robotArm, robotGripper]
            df.loc[i] = [tm2, str(line).split()[1], robotRun, robotArm, robotGripper]
            i += 1

        c = cv2.waitKey(1)
        if c == 27 or robotRun == 'stop':
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return df



if __name__ == "__main__":
    cameraInput = 0
    equalityCoef = 15
    framesInterval = 5
    dirName = sys.argv[1]
    if os.path.exists(dirName):
        os.system('rm -r '+dirName)    
    if not os.path.exists(dirName):
        os.makedirs(dirName)
    checkRequirments()
    # connFile = open('conn.txt','r')
    robotRun = 'N/A'
    print('Waiting for robot')
    while robotRun != 'running':
        robotRun, robotArm, robotGripper = readRobot()
        time.sleep(0.01)
    df = main(dirName)
    # connFile.close()
    getAccuracy(df, equalityCoef)
    df.to_csv(dirName+'/output.csv', index=False)
    genSuggestion(df, dirName, framesInterval)
