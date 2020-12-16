import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
import cv2
MODELPATH = "CL_tflite"

interpreter = tf.lite.Interpreter(model_path=MODELPATH)
input_det = interpreter.get_input_details()
output_det = interpreter.get_output_details()
interpreter.resize_tensor_input(input_det[0]['index'],(1,224,224,3))
interpreter.resize_tensor_input(output_det[0]['index'],(1,4))
interpreter.allocate_tensors()

print(interpreter)
def predictNprepare_image(filepath):
    img = load_img(filepath, target_size=(224, 224))
    img = img_to_array(img) / 255.0
    img = img.reshape([1, 224, 224, 3])
    img_np = np.array(img, dtype=np.float32)
    print(img_np.dtype)
    interpreter.set_tensor(input_det[0]['index'], img_np)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_det[0]['index'])
    print(predictions)
    X1 = predictions[0][0]
    Y1 = predictions[0][1]
    X2 = predictions[0][2]
    Y2 = predictions[0][3]
    print(X1)
    # determine the class label with the largest predicted
    # probability

    img_array = cv2.imread(filepath, cv2.IMREAD_COLOR)
    (h, w) = img_array.shape[:2]
    # scale the predicted bounding box coordinates based on the image
    # dimensions
    X1 = int(X1 * w)
    Y1 = int(Y1 * h)
    X2 = int(X2 * w)
    Y2 = int(Y2 * h)
    print(X1)
    print(X2)
    print(Y1)
    print(Y2)
    # draw the predicted bounding box and class label on the image
    y = Y1 - 10 if Y1 - 10 > 10 else Y1 + 10
    cv2.putText(img_array, "Car", (X1, y), cv2.FONT_HERSHEY_SIMPLEX,
    0.65, (0, 255, 0), 2)
    cv2.rectangle(img_array, (X1, Y1), (X2, Y2),
    (0, 255, 0), 2)
    # show the output image
    cv2.imshow("Output", img_array)
    cv2.waitKey(0)

predictNprepare_image("00002.jpg")
