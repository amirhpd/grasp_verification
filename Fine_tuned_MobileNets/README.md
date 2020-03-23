# Fine tuned MobileNets
## [mobilenets\.ipynb](mobilenets.ipynb)
IPython notebook for generating and training the fine tuned MobileNets Architecture.
The resulting model files are used for the grasp verification tasks.
This code 
* Loads MobileNets model pre-trained on *ImageNet*s from *keras* library.
* Remove last 6 layers of *MobileNets* and adds a Dense layer with 2 outputs.
* Trains only last 12 layers of the model.
* Prints confusion matrix.
* Saves the trained model as *.h5* and *.tflite* files.

## [mobilenets\.h5](mobilenets.h5)
Trained model file from *keras* library. This file contains the detais and 
can be loaded again by *keras* library.

## [mobilenets\.tflite](mobilenets.tflite)
Trained model file converted to *TensorFlow Lite* file format.
