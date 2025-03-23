# Paul Garces Hand Gesture Password

import numpy as np
import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0) # initializing the webcam, 0 means the first webcam which in this case is the laptop's webcam
handSolution = mp.solutions.hands # allows us to use the hand tracking model
hands = handSolution.Hands() # initilizing the hand tracking model
mp_draw = mp.solutions.drawing_utils # drawing the landmarks on the hand, don't have it right now but will be used later
password_array = [] # array to store the hand gestures
finger_tips = [4 , 8, 12, 16, 20] # the id of the finger tips, 4 is for the thumb, 8 is for the index finger, 12 is for the middle finger, 16 is for the ring finger, 20 is for the pinky finger

def finger_tracking(landmarkers):
     current_finger_status = [] # array to store the status of each finger, 1 means the finger is open and up, 0 means the finger is closed (almost like making a fist)
     landmarks = landmarkers.landmark # extracting the landmarks of the hand
     
     if landmarks[finger_tips[0]].x > landmarks[finger_tips[0] - 1].x:
        current_finger_status.append(1)
     else:
        current_finger_status.append(0)
        
     for i in range(1, 5):
          if landmarks[finger_tips[i]].y < landmarks[finger_tips[i] - 2].y - 0.05:
            current_finger_status.append(1)
          else:
            current_finger_status.append(0)
     return current_finger_status

# Checking if the camera is opened successfully
# if the camera is not opened successfully, then it will print "Cannot open camera" and exit
if not cap.isOpened():
    print("Cannot open camera")
    exit()
print("Press 's' to save gesture (max 3 gestures) and 'q' to quit")
while True: # while the camera is open (true)...
    #› ...this is capturing frame by frame continuously in a loop until the user presses 'q' to quit and exit the program
    ret, frame = cap.read() # ret is a boolean variable that returns true if the frame is available and captured, the frame actually stores the frames/images
    if not ret: # if frame wasn't received, then break and exit
        print("Can't receive frame (stream end?). Exiting")
        break
    h, w, _ = frame.shape # getting the height and width of the frame
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # converting the frame to RGB since apparantly mediapipe only accepts RGB images
    results = hands.process(rgb_frame) # this takes and passes the frame which was converted to RGB to the hand tracking model
    # frame is the actual image
    if results.multi_hand_landmarks: # checking if any hands were detected
        for hand in results.multi_hand_landmarks: # looping through each hand that was detected
            mp_draw.draw_landmarks(frame, hand, handSolution.HAND_CONNECTIONS) # drawing the connections between the points on the hand
            gesture = finger_tracking(hand) # getting the status of each finger
                    # point is the position of each of the 21 points on the hand
                    # datapoint_id is the id of the point, ex 0 is for the wrist, 1 is for the thumb, 2 is for the index finger, etc.
            cv.putText(frame, f"Gesture: {gesture}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) # displaying the gesture on the frame
            key = cv.waitKey(1) & 0xFF
            if key == ord('s') and len(password_array) < 3: # if user presses 's' then it will save the gesture
                if len(password_array) < 3: # if the length of the password array is less than 3, then it will append the gesture to the password array
                    password_array.append(gesture)
                    print("Gesture saved")
                else: # if the length of the password array is greater than or equal to 3, then it will print "Max gestures saved"
                    key = cv.waitKey(1) & 0xFF
    cv.imshow('Gesture Setup', frame) # displaying the frame with the points on it
    if cv.waitKey(1) & 0xFF == ord('q'): # if user presses 'q' then it will break and exit
        break
# When everything done, release the capture
cap.release() # turns off the webcam
cv.destroyAllWindows() # closes the popup window
print("Final password array: ", password_array) # prints the final password array