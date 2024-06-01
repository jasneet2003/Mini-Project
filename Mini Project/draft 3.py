import cv2
from pyzbar.pyzbar import decode

def scan_barcodes_from_webcam():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, frame = cap.read()

        # Decode barcodes from the current frame
        barcodes = decode(frame)

        # Draw bounding boxes and decode barcode data
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            text = f"{barcode_type}: {barcode_data}"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            print(f"Found {barcode_type} barcode: {barcode_data}")

        # Display the frame with detected barcodes
        cv2.imshow('Barcode Scanner', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_barcodes_from_webcam()
