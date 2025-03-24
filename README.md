# ✋ Hand Gesture Password

This project is a computer vision-based password system that allow you to use **hand gestures** as your authentication method. Using your webcame, the program captures a sequence of three custom gestures, then verifies that same sequence later to "log you in". If the login is successful, it opens an application: in this case, **Spotify**

---

## 📦 Dependencies

This project uses the following Python libraries:

- **numpy** – for numerical operations
- **opencv-python (cv2)** – for webcam access and video frame handling
- **mediapipe** – for real-time hand landmark detection
- **time** – for managing timed instructions
- **os** – for launching external applications (like Spotify)

---

## 🔁 The Process

**a. Hand Tracking and Finger Status Detection** 
- The code initializes the webcam (`cv.VideoCapture(0)`) and sets up MediaPipe’s hand tracking model.
 - **MediaPipe** detects up to 21 landmark points for each detected hand.
 - A helper function, `finger_tracking()`, examines these landmarks:
    - For the thumb, it checks if the thumb tip (landmark 4) is sufficiently to the right of its adjacent joint (landmark 3) using a small buffer.
    - For the other fingers (index, middle, ring, pinky), it compares the vertical position of the fingertip to a corresponding knuckle (PIP joint) with a tolerance.
    - This function returns a list (for example, `[1, 0, 1, 1, 1]`), where each element represents the status of each finger:
        - **1** means the finger is extended/up
        - **0** means the finger is down/closed

**b. Password Creation Phase**
- When the program starts, the user sees a live webcam feed with on-screen instructions:
    - "Enter 3 gestures to create a password. Please press 's' after each gesture."
- The program processes each frame:
    - It converts the captured frame to RGB for MediaPipe.
    - If a hand is detected, it draws the landmarks (the points and the connections) on the hand.
    - The `finger_tracking()` function is called to generate the current gesture (e.g., `[1, 0, 1, 1, 1]`).
    - This gesture is overlaid on the screen for the user to see.
- When the user presses the **'s'** key, the current gesture is saved to a global list called   `password_array`.
    - The system allows only 3 gestures to be saved.
    - After each saved gesture, a confirmation message such as “Gesture saved” is displayed.
- Once 3 gestures are saved (or if the user quits by pressing **'q'**), the capture stops.


