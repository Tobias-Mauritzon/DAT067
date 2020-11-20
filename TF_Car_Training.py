
from tensorflow.keras import datasets, layers, models
import matplotlib.pyplot as plt
import tensorflow as tf
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
model.add(layers.Conv2D(64, (3,3), activation='relu' , input_shape = (100, 100, 1)))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3,3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))

model.summary()

#Dense network, always flatten before the dense work.
model.add(layers.Flatten())
#model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(3, activation='sigmoid')) # hur stort deta lagret är beror på hur många kategorier man använder, i detta fället är det binärt, dvs hund eller cat. Men om vi har 10 categorier skulle vi därför ha layert med storleken 10

# Bygger ihop modelen, binary_crossentropy kan endast användas i binära fall, dvs två categorier.
model.compile(optimizer="adam", 
            loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
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
model.save('saved_model/car_model')

