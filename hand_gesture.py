# Paul Garces Hand Gesture Password

import numpy as np
import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0) # initializing the webcam, 0 means the first webcam which in this case is the laptop's webcam
handSolution = mp.solutions.hands # allows us to use the hand tracking model
hands = handSolution.Hands() # initilizing the hand tracking model
mp_draw = mp.solutions.drawing_utils # drawing the landmarks on the hand, don't have it right now but will be used later

# Checking if the camera is opened successfully
# if the camera is not opened successfully, then it will print "Cannot open camera" and exit
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True: # while the camera is open (true)...
    # ...this is capturing frame by frame continuously in a loop until the user presses 'q' to quit and exit the program
    ret, frame = cap.read() # ret is a boolean variable that returns true if the frame is available and captured, the frame actually stores the frames/images
    if not ret: # if frame wasn't received, then break and exit
        print("Can't receive frame (stream end?). Exiting")
        break
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # converting the frame to RGB since apparantly mediapipe only accepts RGB images
    results = hands.process(rgb_frame) # this takes and passes the frame which was converted to RGB to the hand tracking model
    # frame is the actual image
    if results.multi_hand_landmarks: # checking if any hands were detected
        for hand in results.multi_hand_landmarks: # looping through each hand that was detected
                for datapoint_id, point in enumerate(hand.landmark): # drawing the 21 dots/points on each of the images for help visually
                    # point is the position of each of the 21 points on the hand
                    # datapoint_id is the id of the point, ex 0 is for the wrist, 1 is for the thumb, 2 is for the index finger, etc.
                    h, w, c = frame.shape # gets the height, width, and channel of the frame
                    x, y = int(point.x * w), int(point.y * h) # converting the x and y coordinates of the point to the actual pixel values
                    cv.circle(frame, (x, y), 5, (255, 0, 255), cv.FILLED) # drawing a circle at the x and y coordinates of the point
    cv.imshow('frame', frame) # displaying the frame with the points on it
    if cv.waitKey(1) == ord('q'): # if user presses 'q' then it will break and exit
        break
# When everything done, release the capture
cap.release() # turns off the webcam
cv.destroyAllWindows() # closes the popup window