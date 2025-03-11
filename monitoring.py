import cv2
import threading
import os
import tkinter as tk
from PIL import Image, ImageTk
from playsound import playsound

# --- GUI Setup ---
root = tk.Tk()
root.title("Drowsiness Detection")

# --- GUI Elements ---
video_label = tk.Label(root)
video_label.pack()

stop_button = tk.Button(root, text="Stop", width=10, bg="red", fg="white")
stop_button.pack(pady=10)

# --- Global Variables and Flags ---
stop_flag = threading.Event()
alarm_on = False
closed_eyes_frame_count = 0
drowsiness_threshold = 120  # Placeholder; will be calculated based on FPS

# --- Load Cascades ---
face_cascade_path = 'haarcascade_frontalface_default.xml'
eye_cascade_path = 'haarcascade_eye.xml'  # Using the basic eye cascade

if not os.path.exists(face_cascade_path):
    print(f"Error: Could not find {face_cascade_path}")
    exit()
if not os.path.exists(eye_cascade_path):
    print(f"Error: Could not find {eye_cascade_path}")
    exit()

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

# --- Initialize Webcam and Get FPS ---
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

fps = cap.get(cv2.CAP_PROP_FPS)
print(f"Webcam FPS: {fps}")

# --- Calculate Drowsiness Threshold (4 seconds) ---
if fps > 0:
    drowsiness_threshold = int(4 * fps)  # Calculate based on 4 seconds
    print(f"Drowsiness threshold set to: {drowsiness_threshold} frames")
else:
    print("Warning: Could not determine FPS. Using default threshold of 120 frames.")
    drowsiness_threshold = 50  # Default for ~30 FPS

# --- Functions ---
def play_alarm():
    global alarm_on
    print("[DEBUG] Alarm thread started!")
    try:
        playsound('alarm.wav')
    except Exception as e:
        print(f"Error playing sound: {e}")
    finally:
        alarm_on = False
        print("[DEBUG] Alarm thread finished!")

def update_video():
    global closed_eyes_frame_count, alarm_on

    if stop_flag.is_set():
        return

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        root.after(10, update_video)
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    eyes_detected = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Eye Detection with Tuning
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(eyes) >= 2:  # Require at least two eyes
            eyes_detected = True
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    if eyes_detected:
        closed_eyes_frame_count = 0
        print("[DEBUG] Eyes detected - Resetting counter")
    else:
        closed_eyes_frame_count += 1
        print(f"[DEBUG] Closed eyes frame count: {closed_eyes_frame_count}")

    if closed_eyes_frame_count >= drowsiness_threshold:
        if not alarm_on:
            alarm_on = True
            print("[DEBUG] Drowsiness detected! Starting alarm thread...")
            threading.Thread(target=play_alarm, daemon=True).start()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    if not stop_flag.is_set():
        root.after(10, update_video)

def stop_capture():
    stop_flag.set()
    cap.release()
    root.destroy()
    print("Stopped")

# --- Bindings ---
stop_button.config(command=stop_capture)
update_video()
root.mainloop()