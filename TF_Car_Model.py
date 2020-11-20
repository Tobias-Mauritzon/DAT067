"""
TF_CAR_Model.py
Laddar in datan från den speciferade databasen och sparar labelsen och featuresen i pickle format som
X.pickle för features
y.pickle för labels.
# Author: Greppe
# Reviewed by:
# Date: 2020-11-20
"""

import numpy as np 
import matplotlib.pyplot as plt
import random
import os
import cv2

DATADIR = "CarData"
CATEGORIES = ["Car", "Dog", "Cat"]

#Skapar Arrayen för träningsdata
training_data = []

#Storlken på Bilderna
IMG_SIZE = 100

"""
Läser in data från den speciferad pathen och omvandlar det till en image array
Använder sig av grå skala.
"""
# Funktion för att skapa datan.
def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category) # path to cats or dogs dir
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass

create_training_data()

#printar storlken på träningsdatan
print(len(training_data))



# Shuffelar datan så att varje epoch får olika ordningar av datan.
random.shuffle(training_data)

# Den tomma arrayen för features (bilder)
X = []
# Den tomma arrayen för labels
y = []

# Lägger labels och featuresen till tränings datan
for features, label in training_data:
    X.append(features)
    y.append(label)

# gör om form och gör det till en numpy array
X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1) # -1 tar alla storlekar, första parameteren skall man specifera storlken
# gör om till en numpy array
y = np.array(y) 

# Exporterar data modellen till pickle formatet, så vi kan träna utan att skapa data modellen varje gång
import pickle
pickle_out = open("X.pickle","wb")
pickle.dump(X, pickle_out)
pickle_out.close()

import pickle
pickle_out = open("y.pickle","wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle","rb")
x = pickle.load(pickle_in)