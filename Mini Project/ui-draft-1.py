import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time
import tkinter as tk
from PIL import Image, ImageTk
import threading

# Function to start barcode scanning
def start_scanning():
    global cap, video_label

    # Start barcode scanning loop
    while True:
        success, img = cap.read()

        # Check for barcode detection
        for barcode in decode(img):
            myData = barcode.data.decode('utf-8')
            barcode_label.config(text=myData)

        # Convert image to RGB format for displaying in Tkinter
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_tk = ImageTk.PhotoImage(image=Image.fromarray(img_rgb))

        # Update video label with the latest frame
        video_label.imgtk = img_tk
        video_label.configure(image=img_tk)

        # Update GUI
        root.update()

        # Delay for smoother video playback (adjust as needed)
        time.sleep(0.03)

# Initialize Tkinter window
root = tk.Tk()
root.title("Barcode Scanner")

# Create video label to display webcam feed
video_label = tk.Label(root)
video_label.pack()

# Create label to display scanned barcode data
barcode_label = tk.Label(root, text="")
barcode_label.pack()

# Specify the index or device ID of the webcam
webcam_index = 0  # Change this to the index of the desired webcam

# Open the specified webcam
cap = cv2.VideoCapture(webcam_index)
cap.set(3, 640)
cap.set(4, 480)

# Start barcode scanning in a separate thread
start_scanning_thread = threading.Thread(target=start_scanning)
start_scanning_thread.start()

# Run the Tkinter event loop
root.mainloop()

# Release the webcam when the Tkinter window is closed
cap.release()
