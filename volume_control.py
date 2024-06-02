# Import necessary libraries
import cv2
import mediapipe as mp
import numpy as np
import math
import time
#below 3 libraries are used for audio control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import *

# Get audio devices and activate the audio interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
vc = cast(interface, POINTER(IAudioEndpointVolume))

# Get the minimum and maximum volume range from the audio interface
Range = vc.GetVolumeRange()
minR, maxR = Range[0], Range[1]

# Initialize the MediaPipe Hands module
mpHands = mp.solutions.hands
Hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
PTime = 0
vol = 0
volBar = 400
volPer = 0

# Open the default camera (camera index 0)
cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    lmList = []  # Initialize a list to store landmarks
    success, img = cap.read()  # Read a frame from the camera
    converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = Hands.process(converted_image)

    if results.multi_hand_landmarks:
        for hand_in_frame in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_in_frame, mpHands.HAND_CONNECTIONS)

            # Collect landmark data
            for id, lm in enumerate(results.multi_hand_landmarks[0].landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([cx, cy])

    if len(lmList) != 0:
        x1, y1 = lmList[4][0], lmList[4][1]
        x2, y2 = lmList[8][0], lmList[8][1]

        # Draw circles and lines on the hand landmarks
        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3, cv2.FILLED)

        # Calculate the length between two points on the hand
        length = math.hypot(x2 - x1 - 30, y2 - y1 - 30)

        # Map the length to volume range and volume bar
        vol = np.interp(length, [50, 300], [minR, maxR])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        # Set the system's master volume level
        vc.SetMasterVolumeLevel(vol, None)

    CTime = time.time()
    fps = 1 / (CTime - PTime)
    PTime = CTime

    # Display the frames per second on the window
    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    # Check if the escape key has been pressed
    if cv2.waitKey(1) == 27:
        break

    cv2.imshow("Hand Tracking", img)

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
