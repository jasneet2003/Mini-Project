import cv2

# Replace the IP address and port number with those from your IP camera app
url = 'http://192.168.29.96:4747/video'
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()

    # Process the frame as desired

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
