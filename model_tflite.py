import tensorflow as tf
import os
MODELNAME = "Cl_tflite_OI"
SAVEDIR = "saved_model/localization_model"
converter = tf.lite.TFLiteConverter.from_saved_model(SAVEDIR) # path to the SavedModel directory
tflite_model = converter.convert()

tflite_model_name = MODELNAME
open(tflite_model_name, "wb").write(tflite_model)