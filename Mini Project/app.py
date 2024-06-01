from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Function to scan barcode
def scan_barcode():
    cap = cv2.VideoCapture(0)
    success, img = cap.read()
    cap.release()

    barcode_data = []
    for barcode in decode(img):
        barcode_data.append(barcode.data.decode('utf-8'))

    return barcode_data

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle barcode scanning
@app.route('/scan', methods=['GET'])
def barcode_scan():
    barcode_data = scan_barcode()
    return jsonify({'barcode_data': barcode_data})

if __name__ == '__main__':
    app.run(debug=True)