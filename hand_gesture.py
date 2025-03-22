# Paul Garces Hand Gesture Password

import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

# Checking if the camera is opened
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True: # while the camera is open (true)...
    # ...this is capturing frame by frame
    ret, frame = cap.read() # ret is a boolean variable that returns true if the frame is available
    # frame is the actual image
    if not ret: # if frame wasn't received, then break and exit
        print("Can't receive frame (stream end?). Exiting")
        break
    # the actual function of the frame is being worked here
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # its converting the frame to grayscale but we'd change it for the password
    # Display the resulting frame
    cv.imshow('frame', frame) # this is creates a popup of the current image in real time
    if cv.waitKey(1) == ord('q'): # if user presses 'q' then it will break and exit
        break
# When everything done, release the capture
cap.release() # turns off the webcam
cv.destroyAllWindows() # closes the popup window