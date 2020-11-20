import os
import cv2

"""
This script is a independant test file for recognition of 
cars with haar cascades.

Author Tobias Mauritzon
Reviewed by: Joachim Antfolk
Date: 2020-11-20
"""

# reading "good" cascade identifier
# you may need to cd in to the correct directory
carCascade = cv2.CascadeClassifier("CascadeRelated/Resources/cars.xml")

# reading "bad" cascade identifier
carCascade2 = cv2.CascadeClassifier("CascadeRelated/Resources/cas4.xml")

# video stream with connected webbcam
cap = cv2.VideoCapture(0)

# video stream with ip cam specific for my network
# cap = cv2.VideoCapture('http://192.168.1.100:8080/video')

cap.set(3, 960)
cap.set(4, 520)

# main program loop exit with q
while (cap.isOpened()):
    # read current image in video stream
    success, img = cap.read()
    success1, imgCar1 = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find obejcts with cascades
    cars = carCascade.detectMultiScale(imgGray, 1.1, 4)
    cars2 = carCascade2.detectMultiScale(imgGray, 1.1, 4)

    # writes rectangel around detected objects in cars
    for(x, y, w, h) in cars:
        cv2.rectangle(imgCar1, (x, y), (x+w, y+h), (255, 0, 0), 1)
        cv2.putText(imgCar1, 'Car', (x, y-5),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    # writes rectangel around objects detected in cars and cars2
    for(x, y, w, h) in cars:
        for(x2, y2, w2, h2) in cars2:
            posOuter = [x + w/2, y + h/2]
            if(posOuter[0] > x2 and posOuter[0] < (x2+w2)):
                if(posOuter[1] > y2 and posOuter[1] < (y2+h2)):

                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)
                    cv2.putText(img, 'Car', (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    # output edited images to window
    cv2.imshow("Car1", imgCar1)
    cv2.imshow("Overlapping", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
