# Paul Garces Hand Gesture Password

# downloading all the packages necessary for this project to work 
import numpy as np
import cv2 as cv
import mediapipe as mp
import time
import os

cap = cv.VideoCapture(0) # initializing the webcam, 0 means the first/default webcam which in this case is the laptop's webcam
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

    # this is for the rest of the fingers, index (#8), middle (#12), ring (#16), and pinky (#20) (1-5 since we're not including the thumb)
    # since these fingers are vertical, if the tip of the finger is higher (y value) than the fingers PIP (knuckle), then the finger is up (1), if not, then finger is down (0)
     for i in range(1, 5):
          if landmarks[finger_tips[i]].y < landmarks[finger_tips[i] - 2].y - 0.05:
            current_finger_status.append(1)
          else:
            current_finger_status.append(0)
     return current_finger_status
    # added buffers to each of the checks to make sure the model isn't too sensitive, like shaking or moving the hand too much
    # adds the state of the fingers to the current_finger_status array and returns it
    # this is all done and checked visually

# Checking if the camera is opened successfully
# if the camera is not opened successfully, then it will print "Cannot open camera" and exit
if not cap.isOpened():
    print("Cannot open camera")
    exit()
print("Press 's' to save gesture (max 3 gestures) and 'q' to quit")

start_time = time.time() # getting the current time when the program starts
instruction_time = 5 # this is setting up the amount of time that the user has to read the instructions, in this case 5 seconds
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
    if time.time() - start_time < instruction_time: # if the current time minus the start time is less than the instruction time, then it will display the instructions
        cv.putText(frame, "Enter 3 gestures to create a password. Please press 's' after each gesture", (10, 80), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2) # displaying the instructions on the actual frame


    if results.multi_hand_landmarks: # checking if any hands were detected
        for hand in results.multi_hand_landmarks: # looping through each hand that was detected
            mp_draw.draw_landmarks(frame, hand, handSolution.HAND_CONNECTIONS) # drawing the connections between the points on the hand
            gesture = finger_tracking(hand) # getting the status/list of which fingers are up and which one arent
            cv.putText(frame, f"Gesture: {gesture}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) # displaying the gesture on the frame, e.g. "Gesture: [1, 0, 1, 1, 1]"
            key = cv.waitKey(1) & 0xFF
            if key == ord('s') and len(password_array) < 3: # if user presses 's' and haven't saved 3 gestures then it will save the current gesture and show "gesture saved" on the frame
                password_array.append(gesture)
                cv.putText(frame, "Gesture saved", (10, 120), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2) # displays "Gesture saved" on the frame
                cv.imshow('Gesture Setup', frame) # displays the frame with the gesture saved message
                cv.waitKey(500) # waits for 500 milliseconds before moving on to the next frame
    cv.imshow('Gesture Setup', frame) # opens the webcam, shows the hand landmarks, and the current gesture on the screen
    key = cv.waitKey(1) & 0xFF
    if key == ord('q') or len(password_array) == 3: # if the user presses 'q' or the length of the password array is 3, then it will break and exit the loop
        break
# When everything done, release the capture
cap.release() # turns off the webcam
cv.destroyAllWindows() # closes the popup window

# login verficication phase
# Open webcam again

input_sequence = [] # creating an array to store the gestures that the user will input during the login phase, will be usede to compare against the password array that was created previously
cap = cv.VideoCapture(0) # initializing the webcam again
login_instruct_show = False # a flag to show the login instructions for a short time
login_time = time.time() # getting the current time when the program starts

#capuring the frames from the webcame again, if the frame is not received, then it will break and exit the loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape # getting the height and width of the frame
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # once again converting it to RGB for mediapipe
    results = hands.process(rgb_frame) # sending the frame to the hand tracking model

    if not login_instruct_show and time.time() - login_time < instruction_time: # if the login instructions haven't been shown and the time is less than the instruction time, then it will display the instructions
        cv.putText(frame, "Enter your 3 gestures to login. Please press 's' after each gesture", (10, 100), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2) # displaying the instructions on the frame for 5 seconds
    else:
        login_instruct_show = True

    #if the hands are detected, then it will draw the landmarks and connections between the points up to the mp.draw_landmarks part
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, handSolution.HAND_CONNECTIONS)
            gesture = finger_tracking(hand) # storing an array of the current gestures, as in which fingers are up and which are down
            cv.putText(frame, f"Gesture: {gesture}", (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2) # displaying the gesture on the frame, like actually printing it on the frame as before

            # if the user presses 's' then it will save the gesture, but only if the length of the input sequence is less than 3
            key = cv.waitKey(1) & 0xFF
            if key == ord('s') and len(input_sequence) < 3: # once again, if the user presses 's' and the length of the input sequence is less than 3, then it will save the currrent gesture
                input_sequence.append(gesture)
                cv.putText(frame, "Gesture saved for login", (10, 130), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) # displaying "Gesture saved" on the frame
                cv.imshow('Login', frame) # displaying the login window
                cv.waitKey(1) # waits for 1 millisecond before moving on to the next frame
    cv.imshow('Login', frame) # opens the webcam, shows the hand landmarks, and the current gesture on the screen

    # Quit login phase if enough (3) gestures or user presses q
    if len(input_sequence) == 3 or cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows() # stop webcam feed and close the popup window

result_show = "Acceess Granted" if input_sequence == password_array else "Access Denied" # if the input sequence is equal to the password array, then it will print "Access Granted", if not, then it will print "Access Denied"
color = (0, 255, 0) if input_sequence == password_array else (0, 0, 255) # if the input sequence is equal to the password array, then it will be green, if not, then it will be red

cap = cv.VideoCapture(0)
ret, frame = cap.read() # start the webcam again and show a single frame with the result
if ret:
    cv.putText(frame, result_show, (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv.imshow("Result", frame)
    cv.waitKey(3000)

cap.release()
cv.destroyAllWindows()

if "Granted" in result_show: # if the result contains "Granted" then it will launch spotify
    os.system("open /Applications/Spotify.app")