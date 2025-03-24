# ✋ Hand Gesture Password with Multi-User Login

This project is a computer vision-based password system that allows users to authenticate themselves using **hand gestures**. It uses your webcam to record a sequence of three custom gestures per user and verifies the same sequence later to allow access. If login is successful, the program allows the user to **open any app** of their choice (via terminal input).

---

## 📦 Dependencies

This project uses the following Python libraries:

- **numpy** – for numerical operations
- **opencv-python (cv2)** – for webcam access and video frame handling
- **mediapipe** – for real-time hand landmark detection
- **time** – for managing timed instructions
- **os** – for launching external applications
- **json** – for saving each user's gesture-based password locally

---

## 🔁 How It Works

### a. Multi-User Login with Gesture Password
- At the start, the user is prompted to enter their name.
- Based on the name, the program looks for a corresponding JSON file (e.g., `paul_gesture_password.json`).
- If the file exists, it loads the user’s saved gesture password for login.
- If it doesn’t, it prompts the user to create a new password using 3 custom gestures.

### b. Hand Tracking and Gesture Detection
- MediaPipe tracks 21 hand landmarks from the webcam input.
- A custom `finger_tracking()` function identifies whether each finger (thumb, index, middle, ring, pinky) is **up** or **down**:
    - Thumb: checks the x-position difference.
    - Other fingers: check the y-position difference between fingertip and knuckle.
- The result is a binary array like `[1, 0, 1, 1, 1]` representing the current gesture.

### c. Password Setup Phase (only once per user)
- If it’s a new user, the system opens the webcam and prompts:
    - "Enter 3 gestures to create a password. Press 's' after each gesture."
- After each saved gesture, a message "Gesture saved" is shown.
- When 3 gestures are recorded, they’re saved as a `.json` file with the user’s name.

### d. Login Phase
- The webcam reopens and asks the user to re-enter their 3 gestures (same order).
- The user presses **'s'** to capture each gesture.
- The captured login gestures are compared to the saved ones.
- If they match → “Access Granted” (green).
- If not → “Access Denied” (red).

### e. Application Launcher
- If login is successful, the user can open any application by typing its name in the terminal:
    - For example: `Spotify`, `Notes`, `Calendar`, etc.
- The user types `'exit'`  in the terminal to end the session.

---

## ❓ How to Use

### 1. Run the Script
- Make sure you’ve installed the dependencies:
  ```bash
  pip install numpy opencv-python mediapipe
  ```
- Run the Python script from your terminal:
  ```bash
  python hand_gesture.py
  ```

### 2. If You’re a New User
- You’ll be asked to enter your name.
- The webcam window titled **"Gesture Setup"** will open.
- Perform a hand gesture and press **'s'** to save — do this 3 times.
- This will then lead you to the **Login** window to re-enter the password, which will allow you access.
- Your gesture password is saved locally in a JSON file (e.g., `alex_gesture_password.json`).

### 3. If You’re a Returning User
- Enter the same name again when prompted.
- The webcam window titled **"Login"** will open.
- Repeat the same 3 gestures and press **'s'** after each.
- If they match your saved password, you’ll get access.

### 4. Launch an App
- Once logged in, type the name of the app in the terminal to open it.
    - Example: `Spotify`, `Notes`, `System Preferences`
- Type `'exit'` in the terminal to end the session.

---

## 💡 Features and Ideas to Extend

- **🔐 User-specific Gesture Passwords**
    - Each user’s password is stored as `username_gesture_password.json`
- **🔄 Retry or Reset Option**
    - Add an option to retry login or reset password
- **🖥️ Custom Dashboard**
    - Instead of terminal input, create a graphical dashboard
- **📁 File Access Control**
    - Use gestures to unlock access to personal folders or files

---

## ✅ Example

```
Enter your name in the terminal: alice
Gesture Setup window opens
→ Press 's' for 3 custom gestures → Password saved as `alice_gesture_password.json`
→ This will lead to the Login window
    → Enter the password again

Next time:
Enter your name in the terminal : alice
Login window opens
→ Do same 3 gestures → Access Granted
→ Enter app name in the terminal: Spotify → Spotify opens
```

---

This project shows how creative computer vision and user interaction can be — gesture-based authentication is just the beginning!