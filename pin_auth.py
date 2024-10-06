import cv2
import time
import mediapipe as mp
from pynput.keyboard import Controller
from pymongo import MongoClient
import pyttsx3

from keys import Key
from handTracker import HandTracker

# Connect to MongoDB
client = MongoClient("mongodb+srv://hemanth182004:h70iVn3ARYS2Hd8o@hemanthcluster1.b0mvbau.mongodb.net/")
db = client["bank"]
collection = db["user"]

def store_pin(username_id, pin):
    try:
        document = {"username_id": username_id, "pin": pin, "balance": 0}
        collection.insert_one(document)
        print(f"Stored PIN for {username_id}")
    except Exception as e:
        print(f"Error storing PIN: {e}")

def retrieve_pin(username_id):
    try:
        document = collection.find_one({"username_id": username_id})
        if document:
            return document["pin"]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving PIN: {e}")
        return None

def pad(string, voice1, voice2):
    face_detection = mp.solutions.face_detection.FaceDetection(0.6)

    def getMousPos(event, x, y, flags, param):
        global clickedX, clickedY
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONUP:
            clickedX, clickedY = x, y
        if event == cv2.EVENT_MOUSEMOVE:
            mouseX, mouseY = x, y

    def detector(frame):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_detection.process(imgRGB)

        if result.detections:
            count = len(result.detections)
        else:
            count = 0

        return count, frame

    z = 1
    a, b = 90, 60
    w, h = 120, 120
    startX, startY = 80, 200
    starta, startb = 800, 130

    keys = []
    letters = list("1234567890")
    positions = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (1, 3)]

    for i, l in enumerate(letters):
        x_offset, y_offset = positions[i]
        keys.append(Key(starta + x_offset * w + x_offset * 6, startb + y_offset * (h + 7), w, h, l))

    keys.append(Key(startX, startY + 230, w + 80, h, "CLEAN"))
    keys.append(Key(startX + 20 + w * 3, startY + 20, w + 130, h, "ENTER"))

    textBox = Key(10 * startX + 20, startY - a - 75, 5 * b + 9 * 5, a, '')

    cap = cv2.VideoCapture(0)
    ptime = 0

    def talk(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    talk(voice1)
    tracker = HandTracker()

    frameHeight, frameWidth, _ = cap.read()[1].shape

    clickedX, clickedY = 0, 0
    mouseX, mouseY = 0, 0
    cv2.namedWindow(string)
    counter = 0
    previousClick = 0

    keyboard = Controller()

    # Variable to store PIN
    pin = ""
    pin_length = 4

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
        frame = tracker.findHands(frame)
        lmList = tracker.getPostion(frame, draw=False)
        if lmList:
            signTipX, signTipY = lmList[7][1], lmList[7][2]
            thumbTipX, thumbTipY = lmList[8][1], lmList[8][2]
            cv2.circle(frame, (thumbTipX, thumbTipY), 10, (0, 255, 0), cv2.FILLED)
        ctime = time.time()
        fps = int(1 / (ctime - ptime))
        cv2.putText(frame, "face" + str(count), (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.putText(frame, str(fps) + " FPS", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        cv2.setMouseCallback(string, getMousPos)

        alpha = 0.5

        textBox.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.3)
        for k in keys:
            if k.isOver or k.isOver(signTipX, signTipY):
                alpha = 0.1
                if k.isOver(clickedX, clickedY):
                    if k.text == 'CLEAN':
                        textBox.text = textBox.text[:-20]
                    elif k.text == 'ENTER':
                        if len(pin) == pin_length:
                            talk("PIN accepted")
                            talk(voice2)
                            store_pin("user123", pin)  # Store the PIN
                            cap.release()
                            cv2.destroyAllWindows()
                            print("PIN entered:", pin)
                        else:
                            talk("Please enter a 4-digit PIN.")
                    else:
                        if len(pin) < pin_length:
                            pin += k.text
                            textBox.text += k.text
                            keyboard.press(k.text)

            if k.isOver(thumbTipX, thumbTipY):
                clickTime = time.time()
                if clickTime - previousClick > 2.0:
                    if k.text == 'ENTER':
                        if len(pin) == pin_length and len(pin) >= pin_length:
                            if pin not in ["1234", "1111", "2123", "2445"]:
                                talk(voice2)
                                store_pin("user123", pin)
                                cap.release()
                                cv2.destroyAllWindows()
                                print("PIN entered:", pin)
                            else:
                                talk("invalid pin")
                        else:
                            talk("Please enter a 4-digit PIN.")
                    elif k.text == 'CLEAN':
                        pin = ""
                        textBox.text = textBox.text[:-20]
                    else:
                        if len(pin) < pin_length:
                            pin += k.text
                            textBox.text += k.text
                            keyboard.press(k.text)
                    previousClick = clickTime

            k.drawKey(frame, (255, 255, 255), (0, 0, 0), alpha=alpha)
            alpha = 0.5
        clickedX, clickedY = 0, 0
        ptime = ctime
        cv2.imshow(string, frame)
        pressedKey = cv2.waitKey(1)
        if pressedKey == ord('d'):
            break

    cap.release()
    cv2.destroyAllWindows()
