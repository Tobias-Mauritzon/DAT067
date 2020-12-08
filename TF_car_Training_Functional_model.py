
"""
TF_CAR_Training.py
Skappar ett CNN som sedan trännas med hjälp av databasen som laddas in av TF_Car_Model
# Author: Greppe
# Reviewed by:
# Date: 2020-11-20
"""
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import tensorflow as tf
from  tensorflow import keras
import pickle
import numpy as np 
import time

# Laddar in trännings datan
X_features = np.array(pickle.load(open("X.pickle", "rb")))
y_labels = np.array(pickle.load(open("y.pickle", "rb")))

# Delar bilderna på 255
X_features = X_features/255.0

# Modellen.
inputs = keras.Input(shape=(128, 128, 3))
x = layers.Conv2D(32, (3,3), activation='relu') (inputs)
x = layers.MaxPooling2D(pool_size=(2, 2))(x)
x = layers.Conv2D(64, (3,3), activation='relu') (x)
x = layers.MaxPooling2D(pool_size=(2, 2))(x)
x = layers.Conv2D(128, (3,3), activation='relu') (x)
x = layers.MaxPooling2D(pool_size=(2, 2))(x)
x = layers.Flatten(name="Flatten_CNN")(x)
x = layers.Dense(64, activation='relu', name="dense_last_layer")(x)
output = layers.Dense(3, activation="softmax")(x)
model = keras.Model(inputs=inputs, outputs=output)

model.summary()

# Bygger ihop modelen, binary_crossentropy kan endast användas i binära fall, dvs två categorier.
model.compile(optimizer=keras.optimizers.Adam(learning_rate=3e-4), 
            loss = keras.losses.SparseCategoricalCrossentropy(from_logits=False),
            metrics=['accuracy'])

#Kör träningen
history = model.fit(X_features, y_labels, batch_size=32, epochs= 10, validation_split= 0.3)

# Definera värden för graferna.
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

#Plotta ut träningen jämnfört med vailderingen.
plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,1.0])
plt.title('Training and Validation Loss')
plt.xlabel('epoch')
plt.show()

#Sparar den tränade modellen så den kan användas.
model.save('saved_model/car_model_v3')
