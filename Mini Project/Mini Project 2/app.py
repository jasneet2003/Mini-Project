from flask import Flask, render_template, Response, request
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime

app = Flask(__name__)

def record_entry(barcode_data):
    # Record the entry with a timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Scanned barcode: {barcode_data}, Timestamp: {timestamp}")
    # Here, you can save the entry to a database or log file
    return f"Scanned barcode: {barcode_data}, Timestamp: {timestamp}"

def scan_barcode(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Use ZBar to detect and decode barcodes
    barcodes = decode(gray)
    
    # Loop over detected barcodes
    for barcode in barcodes:
        # Extract barcode data
        barcode_data = barcode.data.decode("utf-8")
        # Record the entry with a timestamp
        return record_entry(barcode_data)

def generate_frames():
    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            break

        # Detect and decode barcode in the frame
        output = scan_barcode(frame)

        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame and output as a multipart response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n' +
               b'Content-Type: text/plain\r\n\r\n' + output.encode() + b'\r\n')

    # Release the webcam
    cap.release()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)