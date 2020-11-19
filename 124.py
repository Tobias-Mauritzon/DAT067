import numpy as np
import cv2

#Filter som letar efter vad cascaden säger dvs i detta fall frontal face
face_cascade = cv2.CascadeClassifier('cascades/haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('cascades/haarcascade_eye.xml')

#Startar kameran och håller den i gång i X antal sekunder
cap = cv2.VideoCapture(0)


while(True):
    #Capture frame by frame
    ret, frame = cap.read()
    #Convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for(x, y, w, h) in faces:
        # Test för att se om det hittar ett ansikte -> print(x,y,w,h)
        color = (255,0,0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        face_rectangle = cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        #Text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(face_rectangle,"FACE",(x, y-10), font, 0.5, (11,255,255), 2, cv2.LINE_AA)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for(ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh),(0,255,0), 2)

        #detta sparar en bild på ansiktet när videon stängs av
        img_item = "my-image.png"
        cv2.imwrite(img_item, roi_gray)

    #Display resulting frame    
    cv2.imshow('frame', frame)
    
    #Q to stop
    if cv2.waitKey(30) & 0xff ==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
