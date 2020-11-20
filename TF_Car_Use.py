import cv2
import tensorflow as tf
    
CATEGORIES = ["Car", "Dog"]

# Funktion för att ladda in bilder så det går att testa.
def prepare(filepath):
    IMG_SIZE = 100
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

# Laddar in den tidigare tränade modellen.
my_model = tf.keras.models.load_model('saved_model/car_model')

# Testar modellen på en bild av en bil
prediciton = my_model.predict([prepare('car.jpg')])
print(CATEGORIES[int(prediciton[0][0])])

# Testar modellen på en bild av en hund.
prediciton = my_model.predict([prepare('dog.jpg')])
print(CATEGORIES[int(prediciton[0][0])])