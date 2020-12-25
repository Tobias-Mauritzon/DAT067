import tensorflow as tf
import os
MODELNAME = "tflite_caterigorisation"
SAVEDIR = "saved_model/Car_Sign_Lamp_Categorisation_augflipandRot4"
converter = tf.lite.TFLiteConverter.from_saved_model(SAVEDIR) # path to the SavedModel directory
tflite_model = converter.convert()

tflite_model_name = MODELNAME
open(tflite_model_name, "wb").write(tflite_model)