import numpy as np
import cv2

#Filters that are searching for different things, in this case 'cars and numberplates'.
car_cascade = cv2.CascadeClassifier('cascades/cars.xml')
plate_cascade = cv2.CascadeClassifier('cascades/haarcascade_russian_plate_number.xml')

#Starting the camera.
cap = cv2.VideoCapture(0)


while(True):
    #Capture frame by frame
    ret, frame = cap.read()
    #Convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    
    for(x, y, w, h) in cars:
        color = (255,0,0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        #Draws the rectangle around the car
        car_rectangle = cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        
        font = cv2.FONT_HERSHEY_SIMPLEX
        #Display the text
        cv2.putText(car_rectangle,"CAR",(x, y-10), font, 0.5, (11,255,255), 2, cv2.LINE_AA)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        plates = plate_cascade.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in plates:
            #Draws a rectangle within the car rectangle and around the plate
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh),(0,255,0), 2)

    #Display resulting frame    
    cv2.imshow('frame', frame)
    
    #Q to stop
    if cv2.waitKey(30) & 0xff ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()