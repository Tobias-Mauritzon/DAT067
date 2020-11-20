import tensorflow as tf

from tensorflow.keras import datasets, layers, models
import pickle
import numpy as np 
import time

# Laddar in trännings datan
X_features = np.array(pickle.load(open("X.pickle", "rb")))
y_labels = np.array(pickle.load(open("y.pickle", "rb")))

# Delar bilderna på 255
X_features = X_features/255.0

# Modellen.
model = models.Sequential()
#Convulutional network
model.add(layers.Conv2D(64, (3,3), activation='relu' , input_shape =(100, 100,1)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.summary()

#Dense network, always flatten before the dense work.
model.add(layers.Flatten())
#model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid')) # hur stort deta lagret är beror på hur många kategorier man använder, i detta fället är det binärt, dvs hund eller cat. Men om vi har 10 categorier skulle vi därför ha layert med storleken 10

# Bygger ihop modelen, binary_crossentropy kan endast användas i binära fall, dvs två categorier.
model.compile(loss="binary_crossentropy",optimizer="adam", metrics=['accuracy'])

#Kör träningen
model.fit(X_features, y_labels, batch_size=32, epochs= 5, validation_split= 0.3)

#Sparar den tränade modellen så den kan användas.
model.save('saved_model/car_model')

