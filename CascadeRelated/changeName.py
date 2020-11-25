import cv2
import os

c = 1

for filename in os.listdir('NumberPlate/posf3'):

    img = cv2.imread("NumberPlate/posf3/"+filename)

    name = str(c)

    cv2.imwrite('NumberPlate/posf4/' + name, img)

    c = c + 1
