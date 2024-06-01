import cv2
import numpy as np
from pyzbar.pyzbar import decode
import time

# Define a dictionary to store enrollment numbers and corresponding values
student_data = {
    "EN21CS301340": {"Name": "Jasneet", "Address": "Vishnupuri"},
    "EN21CS301331": {"Name": "Ishika Sadhwani", "Address": "Vishal Nagar"},
    "EN21CS301333": {"Name": "Ishika Somani", "Address": "Gumasta Nagar"},
    # Add more entries as needed
}


#img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
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
            print("Enrollment number:", myData)
            
            # Check if the enrollment number is in the student_data dictionary
            if myData in student_data:
                student_info = student_data[myData]
                print("Name:", student_info["Name"])
                print("Address:", student_info["Address"])
                # Add more fields as needed
                
                # Draw bounding box and text for the enrollment number
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect
                cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
            
            # Update the last detection time
            last_detection_time = current_time

    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
