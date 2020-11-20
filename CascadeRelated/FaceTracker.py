import cv2


carCascade = cv2.CascadeClassifier(
    "DAT067/CascadeRelated/Resources/cars.xml")

carCascade2 = cv2.CascadeClassifier(
    "Dat067/CascadeRelated/Resources/cas4.xml")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture('http://192.168.1.100:8080/video')

cap.set(3, 960)
cap.set(4, 520)

while (cap.isOpened()):
    success, img = cap.read()
    #imgCanny = cv2.Canny(img, 150, 200)

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cars = carCascade.detectMultiScale(imgGray, 1.1, 4)
    cars2 = carCascade2.detectMultiScale(imgGray, 1.1, 4)

    for(x, y, w, h) in cars:
        for(x2, y2, w2, h2) in cars2:
            posOuter = [x + w/2, y + h/2]
            if(posOuter[0] > x2 and posOuter[0] < (x2+w2)):
                if(posOuter[1] > y2 and posOuter[1] < (y2+h2)):

                    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)
                    cv2.putText(img, 'Car', (x, y-5),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Video", img)
    # cv2.waitKey(25)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
