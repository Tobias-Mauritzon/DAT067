import numpy as np
import cv2

# Filters that are searching for different things, in this case 'the front of the face and the eyes'
car_cascade = cv2.CascadeClassifier('Resources/cars.xml')
plate_cascade = cv2.CascadeClassifier("Resources/cascade3/cascade3.xml")

# Starting the camera.
cap = cv2.VideoCapture(0)


while(True):
    # Capture frame by frame
    ret, frame = cap.read()
    # Convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(
        gray, 1.1, 4)

    for(x, y, w, h) in cars:
        color = (255, 0, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h

        faceFound = False

        roi_gray = gray[y:end_cord_y, x:end_cord_x]
        roi_color = frame[y:end_cord_y, x:end_cord_x]
        plates = plate_cascade.detectMultiScale(roi_gray, 1.1, 4)
        for(ex, ey, ew, eh) in plates:
            print("found plate")

            faceFound = True

            # Draws a rectangle within the car and around the plate
            cv2.rectangle(frame, (x+ex, y+ey),
                          (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

        if faceFound:
            # Draws the rectangle around the face
            face_rectangle = cv2.rectangle(
                frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

            font = cv2.FONT_HERSHEY_SIMPLEX
            # Display the text
            cv2.putText(frame, "PL in CAR", (x, y-10), font,
                        0.5, (11, 255, 255), 2, cv2.LINE_AA)

    # Display resulting frame
    cv2.imshow('frame', frame)

    # Q to stop
    if cv2.waitKey(30) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
