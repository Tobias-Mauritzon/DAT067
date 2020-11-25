import cv2
import os

c = 1
# felt lika a god when i got this thing to work
# file path in to the folder where the files whose name you want to change are located
for filename in os.listdir('NumberPlate/posf3'):

    img = cv2.imread("NumberPlate/posf3/"+filename)

    # new file path including name and tpye
    name = "NumberPlate/posf4/" + str(c) + "." + filename.split('.')[1]

    cv2.imwrite(name, img)

    c = c + 1
