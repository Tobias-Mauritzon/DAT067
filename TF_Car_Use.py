
"""
TF_CAR_Training.py
Använder den tränade modellen från TF_Car_training för att avgöra vad dem speciferade bilderna har för kategori
# Author: Greppe
# Reviewed by:
# Date: 2020-11-20
"""
import cv2
import os
import tensorflow as tf
    
CATEGORIES = ["Car", "Lamppost", "Sign"]

# Funktion för att ladda in bilder så det går att testa.
def prepare(filepath):
    IMG_SIZE = 128
    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 3)

def check_categeori(prediction):
    if (int(prediciton[0][0]) >= 0.5):
        print("Car")
    elif (int(prediciton[0][1]) >= 0.5):
        print("Lamppost")
    elif (int(prediciton[0][2]) >= 0.5):
        print("Sign")
    else:
        print("Not a Car, Lampost or a Sign")
    return
# Laddar in den tidigare tränade modellen.
my_model = tf.keras.models.load_model('saved_model/Car_Sign_Lamp_Categorisation_augflipandrot4')

# Testar modellen på en bild av en bil
prediciton = my_model.predict([prepare('car.jpg')])
print('car.jpg')
check_categeori(prediciton)

# Testar modellen på en bild av en hund
prediciton = my_model.predict([prepare('lampa.jpg')])
print('lampa.jpg')
check_categeori(prediciton)

# Testar modellen på en bild av en katt
prediciton = my_model.predict([prepare('skylt.jpg')])
print('skylt.jpg')
check_categeori(prediciton)
