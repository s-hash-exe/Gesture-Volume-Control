import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5, modelComplexity=1):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.modelComplex=modelComplexity
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255),-1)
        return lmList





def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        ret, img = cap.read()
        img = detector.findHands(img)
        lmLsit = detector.findPosition(img)
        if len(lmLsit)!=0:
            print(lmLsit[0])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

if __name__ == "__main__":
    main()