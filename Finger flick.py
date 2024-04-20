import tkinter as tk
from tkinter import messagebox
import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# variables
width, height = 1280, 720
gestureThreshold = 500
volume = 50
prev_cx = 0
volume_increment = 5
detector = HandDetector(detectionCon=0.8, maxHands=1)
cap = None  # Placeholder for the video capture object

# Function to start the gesture control
def start_gesture_control():
    global cap
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            cx, cy = hand['center']

            if cy <= gestureThreshold:
                if fingers == [1, 0, 0, 0, 0]:  # up scroll
                    pyautogui.scroll(-100)
                elif fingers == [0, 0, 0, 0, 1]:  # down scroll
                    pyautogui.scroll(100)
                elif fingers == [1, 0, 1, 1, 1]:  # volume control
                    cx_diff = cx - prev_cx
                    volume_change = cx_diff / 10 * volume_increment
                    if volume_change > 0:
                        pyautogui.press('volumeup')
                    elif volume_change < 0:
                        pyautogui.press('volumedown')
                elif fingers == [0, 1, 0, 0, 0]:  # cursor movement
                    cursor_x = int((cx / width) * pyautogui.size().width)
                    cursor_y = int((cy / height) * pyautogui.size().height)
                    pyautogui.moveTo(cursor_x, cursor_y, duration=0.5)
                elif fingers == [0, 1, 1, 0, 0]:  # click
                    pyautogui.click()

            prev_cx = cx

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to stop the gesture control
def stop_gesture_control():
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
    else:
        messagebox.showinfo("Info", "FINGER FLICK is not running.")

# Create the main window
root = tk.Tk()
root.title("FINGER FLICK")

# Set window size and center it on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Load background image
background_image = tk.PhotoImage(file="cat_drawing_bigeyed_11146_800x600.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create Start and Stop buttons
start_button = tk.Button(root, text="Start", command=start_gesture_control)
start_button.place(relx=0.5, rely=0.4, anchor="center")

stop_button = tk.Button(root, text="Stop", command=stop_gesture_control)
stop_button.place(relx=0.5, rely=0.6, anchor="center")

# Run the application
root.mainloop()
