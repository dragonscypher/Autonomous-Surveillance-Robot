
import cv2
import serial
import time
import numpy as np
from tkinter import Tk, filedialog, Button, Label
import os
import threading
from gpiozero import LED

# Load face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Function to upload target image
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        label.configure(text=os.path.basename(file_path))
        global target_image, descriptors_target
        target_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        keypoints_target, descriptors_target = orb.detectAndCompute(target_image, None)

# GUI setup
root = Tk()
root.title("Hexapod Target Image Uploader")
label = Label(root, text="Upload target image to start")
label.pack()
Button(root, text="Upload Image", command=upload_image).pack()

orb = cv2.ORB_create()
keypoints_target = descriptors_target = None

# Initialize serial communication with Arduino
arduino_serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.1)
time.sleep(2)

# Initialize LED
led = LED(17)  # Pin 17 for LED control

cap = cv2.VideoCapture(0)  # Start video capture

def detect_and_send():
    while True:
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)

        # Feature matching with ORB
        if target_image is not None and descriptors_target is not None:
            keypoints_frame, descriptors_frame = orb.detectAndCompute(gray_frame, None)
            if descriptors_frame is not None:
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(descriptors_target, descriptors_frame)
                matches = sorted(matches, key=lambda x: x.distance)

                if len(matches) > 10:  # If enough features match, consider it as the target face
                    for (x, y, w, h) in faces:
                        center_x, center_y = x + w // 2, y + h // 2
                        distance = calculate_distance(w)  # Approximate distance based on face width
                        command = f'X{center_x}Y{center_y}D{distance}'
                        arduino_serial.write(command.encode())

                        # Blink LED faster as it gets closer
                        if distance < 50:
                            led.blink(on_time=0.1, off_time=0.1)
                        else:
                            led.blink(on_time=0.5, off_time=0.5)

                        # Draw the detected face and its center
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def calculate_distance(face_width):
    # Assuming a known width of the face and camera calibration parameters
    KNOWN_WIDTH = 14.0  # Average face width in cm
    FOCAL_LENGTH = 500  # Focal length of the camera
    return (KNOWN_WIDTH * FOCAL_LENGTH) / face_width

def periodic_video_check():
    while True:
        time.sleep(60)  # Wait for one minute
        detect_and_send()

# Run both detection and periodic check in parallel
threading.Thread(target=periodic_video_check, daemon=True).start()
threading.Thread(target=detect_and_send, daemon=True).start()

Button(root, text="Start Detection", command=lambda: threading.Thread(target=detect_and_send, daemon=True).start()).pack()
root.mainloop()
