import cv2
import os

# felt lika a god when i got this thing to work
# file path in to the folder where the files whose name you want to change are located
for filename in os.listdir('NumberPlate/posf4'):

    img = cv2.imread("NumberPlate/posf4/"+filename)

    # new file path including name and tpye
    height, width, dim = img.shape

    if height < 50 or height < 50:
        print(img.shape)
        print(filename)
