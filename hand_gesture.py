# Paul Garces Hand Gesture Password

import numpy as np
import cv2 as cv
import mediapipe as mp
import time

cap = cv.VideoCapture(0) # initializing the webcam, 0 means the first webcam which in this case is the laptop's webcam
handSolution = mp.solutions.hands # allows us to use the hand tracking model
hands = handSolution.Hands() # initilizing the hand tracking model
mp_draw = mp.solutions.drawing_utils # drawing the landmarks on the hand, don't have it right now but will be used later
password_array = [] # array to store the users created password with gestures
finger_tips = [4 , 8, 12, 16, 20] # the id of the 5 finger tips, 4 is for the tip of the thumb, 8 is for the tip of the index finger, 12 is for the tip of  middle finger,
# 16 is for the tip of the ring finger, 20 is for the tip of the pinky finger

def finger_tracking(landmarkers): # this function is checking which fingers are up and which are down
     current_finger_status = [] # array to store the status of each finger, 1 means the finger is open and up, 0 means the finger is closed (almost like making a fist)
     landmarks = landmarkers.landmark # extracting all the 21 landmark points
     
     #so since the thumb is different from the other fingers, meaning doing a [1, 1, 1, 1, 1] gesture, then the thumb is on its side
     # so for the right hand, if the the thumb tip is further to the right than #3 (thumb_ip) then the thumb is up
     if landmarks[finger_tips[0]].x > landmarks[finger_tips[0] - 1].x - 0.01:
        current_finger_status.append(1)
     else:
        current_finger_status.append(0)

    # this is for the rest of the fingers, index, middle, ring, and pinky (1-5 since we're not including the thumb)
    # since these fingers are vertical, if the tip of the finger is higher (y value) than the fingers PIP (knuckle), then the finger is up (1), if not, then finger is down (0)
     for i in range(1, 5):
          if landmarks[finger_tips[i]].y < landmarks[finger_tips[i] - 2].y - 0.05:
            current_finger_status.append(1)
          else:
            current_finger_status.append(0)
     return current_finger_status
    #added buffeeers to each of the checks to make sure the model isn't too sensitive
    # adds the state of the fingers to the current_finger_status array and returns it
    # this is all done and checked visually

# Checking if the camera is opened successfully
# if the camera is not opened successfully, then it will print "Cannot open camera" and exit
if not cap.isOpened():
    print("Cannot open camera")
    exit()
print("Press 's' to save gesture (max 3 gestures) and 'q' to quit")
while True: # while the camera is open (true)...
    #› ...this is capturing frame by frame continuously in a loop until the user presses 'q' to quit and exit the program
    ret, frame = cap.read() # ret is a boolean variable that returns true if the frame was read sucessfully, the frame actually stores the frames/images
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
            gesture = finger_tracking(hand) # getting the status/list of which fingers are up and which one arent
            cv.putText(frame, f"Gesture: {gesture}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) # displaying the gesture on the frame, ex "Gesture: [1, 0, 1, 1, 1]"
            key = cv.waitKey(1) & 0xFF
            if key == ord('s') and len(password_array) < 3: # if user presses 's' then it will save the gesture
                if len(password_array) < 3: # if the length of the password array is less than 3, then it will append the gesture to the password array
                    password_array.append(gesture) # adds the gesture to the password array
                    print("Gesture saved")
                else: # if the length of the password array is greater than or equal to 3, then it will print "Max gestures saved"
                    key = cv.waitKey(1) & 0xFF
    cv.imshow('Gesture Setup', frame) # displaying the frame, landmarks, and gesture info on the screen
    if cv.waitKey(1) & 0xFF == ord('q'): # if user presses 'q' then it will break and exit
        break
# When everything done, release the capture
cap.release() # turns off the webcam
cv.destroyAllWindows() # closes the popup window
print("Final password array: ", password_array) # prints the final password array