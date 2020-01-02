'''
Converts .h5 model file to .tflite and .kmodel files
Software License Agreement (MIT License)
Copyright (c) 2020, Amirhossein Pakdaman.
'''
import tensorflow as tf
import os
datasetPath = './dataset_small'
print('  ')
print('  ')
print('Converting to tflite...')
converter = tf.lite.TFLiteConverter.from_keras_model_file('model.h5')
tflite_model = converter.convert()
open("model.tflite", "wb").write(tflite_model)
print('  ')
print('  ')
print('Converting to kmodel...')
os.system("./nncase/ncc -i tflite -o k210model --dataset " + datasetPath + " ./model.tflite ./model.kmodel")

