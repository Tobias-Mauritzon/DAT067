import numpy as np 
import matplotlib.pyplot as plt
import os
import cv2

DATADIR = "CarData"
CATEGORIES = ["Car", "Dog"]

# Visar en bild för att testa inladningen.
for category in CATEGORIES:
    path = os.path.join(DATADIR, category) # path to cats or dogs dir
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
        #plt.imshow(img_array, cmap="gray")
        #plt.show()
        break
    break
print(img_array.shape)
IMG_SIZE = 100

new_array = cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
plt.imshow(new_array, cmap = 'gray')
plt.show()

#training_data = []

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

print(len(training_data))

import random

# Shuffelar datan så att varje epoch får olika ordningar av datan.
random.shuffle(training_data)

for sample in training_data:
    print(sample[1])

X = []
y = []

# Lägger labels och featuresen till tränings datan
for features, label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1) # -1 tar alla storlekar, första parameteren skall man specifera storlken
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