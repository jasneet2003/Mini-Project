from flask import Flask, render_template, Response
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

app = Flask(__name__)

# Function to read frames from the webcam and perform barcode scanning
def read_frames():
    # Specify the index or device ID of the desired webcam
    webcam_index = 0  # Change this to the index of the webcam you want to use (e.g., 0 for the first webcam, 1 for the second webcam, and so on)

    # Open the specified webcam
    cap = cv2.VideoCapture(webcam_index)
    cap.set(3, 640)
    cap.set(4, 480)

    cooldown_period = 5  # Set the cooldown period in seconds
    last_detection_time = time.time()

    while True:
        success, img = cap.read()
        current_time = time.time()

        # Check if enough time has passed since the last detection
        if current_time - last_detection_time > cooldown_period:
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                print(myData)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
                
                # Update the last detection time
                last_detection_time = current_time

        # Encode frame as JPEG
        _, frame = cv2.imencode('.jpg', img)
        frame_bytes = frame.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for video feed and barcode scanning
@app.route('/video_feed')
def video_feed():
    return Response(read_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
