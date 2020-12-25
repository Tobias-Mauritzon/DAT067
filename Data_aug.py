from numpy import expand_dims
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import cv2
from matplotlib import pyplot

filepath = 'Car.jpg'
img = load_img(filepath)
data = img_to_array(img)
samples = expand_dims(data, 0)

#rotation

img = cv2.imread(filepath, cv2.IMREAD_COLOR)
(h, w) = img.shape[:2]
#horizontal move
datagen = ImageDataGenerator(rotation_range=90, width_shift_range=[-(w/5),(w/5)],horizontal_flip=True,brightness_range=[0.2,1.0])
it = datagen.flow(samples, batch_size=1)

datagenZoom = ImageDataGenerator()

for i in range(9):
    pyplot.subplot(330 + 1 + i)


    batch = it.next()

    
    image = batch[0].astype('uint8')
    pyplot.imshow(image)

pyplot.show()