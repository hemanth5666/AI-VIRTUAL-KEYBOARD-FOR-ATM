import time
from keys import *
from handTracker import *
from falcon import *
import mediapipe as mp
face_detection = mp.solutions.face_detection.FaceDetection(0.6)

def getMousPos(event, x, y, flags, param):
    global clickedX, clickedY
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
        mouseX, mouseY = x, y


def detector(frame):
    count = 0
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_detection.process(imgRGB)
    try:
        for count, detection in enumerate(result.detections):
            pass
        count += 1
    except:
        pass
    return count, frame


def pad(balance, string, string1):
    z = 1
    a, b = 90, 60
    w, h = 120, 120
    startX, startY = 80, 200
    starta, startb = 800, 130
    keys = []
    keys.append(Key(startX, startY + 230, w + 80, h, "EXIT"))

    cap = cv2.VideoCapture(0)
    ptime = 0

    tracker = HandTracker()

    frameHeight, frameWidth, _ = cap.read()[1].shape

    clickedX, clickedY = 0, 0
    mousX, mousY = 0, 0
    cv2.namedWindow(string)
    counter = 0
    previousClick = 0

    keyboard = Controller()
    while True:
        ret, frame = cap.read()
        try:
            count, output = detector(frame)
        except:
            pass
        if counter > 0:
            counter -= 1

        signTipX = 0
        signTipY = 0

        thumbTipX = 0
        thumbTipY = 0


        if not ret:
            break
        frame = cv2.resize(frame, (1366, 768))
        frame = cv2.flip(frame, 1)
        # find hands
        frame = tracker.findHands(frame)
        lmList = tracker.getPostion(frame, draw=False)
        if lmList:
            signTipX, signTipY = lmList[7][1], lmList[7][2]
            thumbTipX, thumbTipY = lmList[8][1], lmList[8][2]
        ctime = time.time()
        fps = int(1 / (ctime - ptime))
        cv2.putText(frame, "face" + str(count), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        cv2.putText(frame, str(fps) + " FPS", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(frame, string1 + str(balance), (500, 300), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 0), 6)

        cv2.setMouseCallback(string, getMousPos)

        # checking if sign finger is over a key and if click happens
        alpha = 0.5

        cv2.circle(frame, (thumbTipX, thumbTipY), 10, (0, 255, 0), cv2.FILLED)
        for k in keys:
            if k.isOver or k.isOver(signTipX, signTipY):
                alpha = 0.1
                # writing using mouse right click
                if k.isOver(clickedX, clickedY):
                    if k.text == 'EXIT':
                        cap.release()
                        cv2.destroyAllWindows()
                    else:
                        None

            if k.isOver(thumbTipX, thumbTipY):
                clickTime = time.time()
                if clickTime - previousClick > 2.0:
                    if k.text == 'EXIT':

                        cap.release()
                        cv2.destroyAllWindows()
                    else:
                        None
                    previousClick = clickTime

            k.drawKey(frame, (255, 255, 255), (0, 0, 0))  #, alpha=alpha
            alpha = 0.5
        clickedX, clickedY = 0, 0
        ptime = ctime
        cv2.imshow(string, frame)
                    ## stop the video when 'q' is pressed
        pressedKey = cv2.waitKey(1)
        if pressedKey == ord('d'):
            break

    cap.release()
    cv2.destroyAllWindows()


