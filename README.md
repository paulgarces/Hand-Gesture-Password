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

**c. Login Verification Phase**
- After password creation, the system enters the login phase.
- The webcam reopens, and the user is instructed:
    - "Enter your 3 gestures to login. Please press 's' after each gesture."
- The process is similar:
    - The program captures frames and detects the hand.
    - For each detected hand, it calculates the current gesture and displays it.
    - The user presses **'s'** to save each gesture into an `input_sequence` list.
- When 3 gestures are captured (or the user presses **'q'**), the system compares   `input_sequence` (the login gesture) with `password_array` (the saved password).
    - If they match, the result “Access Granted” is shown (in green); otherwise, “Access Denied” (in red).

**d. Application Launch**
- If the login is successful (i.e., the entered gesture sequence exactly matches the saved password), the program launches Spotify using a system command (you can change the section below in the code to open any application or folder/file):
    - `os.system("open /Applications/Spotify.app")` (This command is tailored for macOS.)

---

# ❓ How to Use?
1. Run the Script:
    - Ensure your webcam is connected and the necessary packages are installed.
    - Run the Python script from your terminal or your preferred IDE (such as VS Code).

2. Set Up Your Password:
    - The webcam window titled **"Gesture Setup"** will open.
    - Follow the on-screen instructions (visible for 5 seconds):
        - "Enter 3 gestures to create a password. Please press 's' after each gesture."
    - Position your right hand in front of the camera. When a hand is detected, the system shows the current gesture (a list of 1s and 0s).
    - Press **'s'** to save each gesture. You must save 3 gestures. A “Gesture saved” message will appear after each save.
    - You can press **'q'** to exit early (but then you won't have a complete password).

3. Login Phase:
    - After the password is set, the webcam reopens in a new window titled **"Login"**.
    - You’ll see an instruction on screen (for about 5 seconds):
        - "Enter your 3 gestures to login. Please press 's' after each gesture."
    - Repeat the same 3 gestures in the same order.
    - Press **'s'** after each gesture to capture them.
    - When 3 gestures are captured, the system compares your input to the saved password.

4. Result & App Launch:
    - The result (either “Access Granted” or “Access Denied”) is displayed on screen for 500 milliseconds.
    - If access is granted, Spotify will launch automatically.

---

# 💭 Future Directions and Ideas
- Change the Launched Application:
    - Modify the system command at the end to launch any app of your choice.

- Improve the UI:
    - Enhance the on-screen instructions or add additional feedback using OpenCV’s drawing functions.

- Persistent Password Storage:
    - Save the password_array to a file (using JSON) so the password persists between sessions.

- Retry Mechanism:
    - Add a mechanism to allow multiple login attempts or lock out after too many failed attempts.