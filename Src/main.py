import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui
import math

# pycaw(python core audio window library)
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# print(volume.GetVolumeRange()) #(-65.25, 0.0)# this will give range of volume by default that is there.

# accessing of camera
cap = cv2.VideoCapture(0)

# gives size of screen
screen_width, screen_height = pyautogui.size()

index_y = 0
index_x = 0
pinky_y = 0
thumb_x = 0
thumb_y = 0

# file getting landmarks, having value of max hands as well
mpHands = mp.solutions.hands

# false since, video stream is better than keeping static image as true
hands = mpHands.Hands(static_image_mode=False,
                      max_num_hands=1,
                      min_detection_confidence=0.2,
                      min_tracking_confidence=0.2)

# utiles required for drawing colors
mpDraw = mp.solutions.drawing_utils

# previous time, captured time (fps)
pTime = 0
cTime = 0

while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)

    # h, w= frame height, width
    h, w, _ = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm) #loop for each id giving specific landmarks
                h, w, c = img.shape

                # cx, cy are the positions of finger tips, related to line 55
                cx = int(lm.x * w)
                cy = int(lm.y * h)
                if id == 8:
                    cv2.circle(img, center=(cx, cy), radius=10, color=(0, 255, 255))
                    index_x = screen_width / w * cx
                    index_y = screen_height / h * cy
                    pyautogui.moveTo(index_x, index_y)

                    # this will give id=8 as pink holed circle
                    # cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)

                    # landmark with lines
                    # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                if id == 12:
                    cv2.circle(img, center=(cx, cy), radius=10, color=(0, 255, 255))
                    middle_x = screen_width / w * cx
                    middle_y = screen_height / h * cy
                    # print('outside',abs(index_y-middle_y)) #related to y co-ordinate
                    if abs(middle_x - index_x) < 40 and abs(middle_y - index_y) < 40:
                        pyautogui.click()
                        pyautogui.sleep(1)
                        print("click")
                if id == 4:
                    cv2.circle(img, center=(cx, cy), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / w * cx
                    thumb_y = screen_height / h * cy
                if id == 20:
                    cv2.circle(img, center=(cx, cy), radius=10, color=(0, 255, 255))
                    pinky_x = screen_width / w * cx
                    pinky_y = screen_height / h * cy
                if id == 17:
                    cv2.circle(img, center=(cx, cy), radius=10, color=(0, 255, 255))
                    pinky17_x = screen_width / w * cx
                    pinky17_y = screen_height / h * cy
                    if abs(pinky_y - pinky17_y) < 40:
                        # hypot is hypotenuse(perpendicular, base)
                        length = math.hypot(index_x - thumb_x, index_y - thumb_y)
                        # print("length",length)

                        # 50 is the difference dist. bet thumb and index finger and length is directly proportional to volume value
                        volumeValue = np.interp(length, [50, 300], [-65.25, 0.0])
                        volume.SetMasterVolumeLevel(volumeValue, None)

                        # converted max and min value of volume to percentage
                        volume_value = ((int(volumeValue) + 65.25) / 65.25) * 100
                        print(int(volume_value))

                        # cv2.line(img,(index_x,index_y),(thumb_x,thumb_y),(255,0,255), 10)
                        # cv2.circle(img, (thumb_x,thumb_y), 15, (0,0,0), cv2.FILLED)
                        # cv2.circle(img, (index_x,index_y), 15, (0,0,0), cv2.FILLED)

                        # this will give landmarks with lines
                        # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)



