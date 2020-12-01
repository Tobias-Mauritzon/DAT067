import numpy as np
import cv2

#Filters that are searching for different things, in this case a numberplate
plate_cascade = cv2.CascadeClassifier('cascades/haarcascade_russian_plate_number.xml')

#Starting the camera.
cap = cv2.VideoCapture(0)


while(True):
    #Capture frame by frame
    ret, frame = cap.read()

    #Convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    
    for(x, y, w, h) in plates:
        color = (255,0,0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        #Draws the rectangle around the numberplate
        plate_rectangle = cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        
        font = cv2.FONT_HERSHEY_SIMPLEX
        #Display the text
        cv2.putText(plate_rectangle,"CAR",(x, y-10), font, 0.5, (11,255,255), 2, cv2.LINE_AA)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]


        #Saves a picture of the last numberplate seen when the application is closed
        img_item = "lastPlate.png"
        cv2.imwrite(img_item, roi_gray)

    #Display resulting frame    
    cv2.imshow('frame', frame)
    
    #Q to stop
    if cv2.waitKey(30) & 0xff ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()