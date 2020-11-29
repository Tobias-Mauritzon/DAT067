import cv2


i = 12

while i > 0:

    img = cv2.imread("Resources/DemoPhotos/p2.PNG")

    plate = cv2.CascadeClassifier(
        "Resources/cascade"+str(i)+"/cascade"+str(i)+".xml")

    imgGray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate.detectMultiScale(imgGray2, 1.1, 4)

    for(x, y, w, h) in plates:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 1)
        cv2.putText(img, 'Plate', (x, y-5),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Frame", img)
    cv2.waitKey(8000)

    cv2.imwrite("Resources/DemoPhotos/Cascade"+str(i)+"_P2.PNG", img)
    i = i - 1
