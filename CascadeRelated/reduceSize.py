import cv2
import os

for filename in os.listdir('NumberPlate/posf2'):

    img = cv2.imread("NumberPlate/posf2/"+filename)

    height, width, dim = img.shape
    height = int(height/2)
    width = int(width/2)

    img = cv2.resize(img, (width, height))

    #saveLoc = ('NumberPlate/posf3/' + filename)

    cv2.imwrite('NumberPlate/posf3/' + filename, img)
