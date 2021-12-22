import cv2
import numpy as np
import time
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

##########################
wCam, hCam = 640, 480
cTime, pTime = 0, 0
##########################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7)

########### System Volume Modifier ############

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar = 400
volPer = 0
#######################

while True:
    ret, img = cap.read()
    img = detector.findHands(img, True)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # Landmark value of thumb tip and index finger tip
        # thump tip location
        x1, y1 = lmList[4][1], lmList[4][2]
        # index finger location
        x2, y2 = lmList[8][1], lmList[8][2]
        cv2.circle(img, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 2)
        # center of line
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (cx, cy), 8, (255, 0, 255), cv2.FILLED)
        # length of the line
        length = math.hypot(x2-x1,y2-y1)

        # Hand Range : 25-200
        # Volume Range : -65 - 0

        vol = np.interp(length,[20,220],[minVol,maxVol])
        volBar = np.interp(length, [20,220], [400,150])
        volPer = np.interp(length, [20, 220], [0,100])
        print(length, vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<25:
            cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50,150),(85,400),(0,128,0), 3)
    cv2.rectangle(img, (53, int(volBar)+3), (82, 397), (0,170,0), cv2.FILLED)
    cv2.putText(img, str(int(volPer))+"%", (50, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1, (0,128,0), 2)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, "FPS: "+str(int(fps)), (20,30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                1, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()