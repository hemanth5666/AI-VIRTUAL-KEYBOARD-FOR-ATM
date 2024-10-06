import mediapipe as mp
import cv2

class HandTracker():
    def __init__(self, detection_con=0.5, max_hands=2, tracking_con=0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(min_detection_confidence=detection_con,
                                        max_num_hands=max_hands, min_tracking_confidence=tracking_con)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if draw:
            self.draw_landmarks(img)
        return img

    def draw_landmarks(self, img):
        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, handLm, self.mpHands.HAND_CONNECTIONS)

    def getPostion(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            h, w, _ = img.shape
            for id, lm in enumerate(myHand.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        return lmList
