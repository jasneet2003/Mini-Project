from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

app = Flask(__name__)

# Specify the index or device ID of the desired webcam
webcam_index = 0  # Change this to the index of the webcam you want to use (e.g., 0 for the first webcam, 1 for the second webcam, and so on)

# Function to start barcode scanning
def start_scanning():
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
            barcode_data = []
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                barcode_data.append(myData)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
                
                # Update the last detection time
                last_detection_time = current_time

            # Send scanned barcode data to HTML template
            yield (b'--barcode_data\r\n'
                   b'Content-Type: text/javascript\r\n\r\n' + 
                   b'<script>updateBarcodeData(["' + 
                   b'", "'.join(data.encode() for data in barcode_data) + 
                   b'"]);</script>' + b'\r\n')

        # Encode the frame as JPEG and return it
        _, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        
        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to start barcode scanning
@app.route('/scan')
def scan():
    return Response(start_scanning(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
