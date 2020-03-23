# Single Block ResNet
## [resnet\.ipynb](resnet.ipynb)
IPython notebook for generating and training the single block ResNet Architecture.
The resulting model files are used for the grasp verification tasks.
This code 
* Loads *ResNet* model from *keras* library.
* Turns 50-layer *ResNet* to 1-layer.
* Trains the model.
* Prints confusion matrix.
* Saves the trained model as *.h5* and *.tflite* files.

## [resnet\.h5](resnet.h5)
Trained model file from *keras* library. This file contains the detais and 
can be loaded again by *keras* library.

## [resnet\.tflite](resnet.tflite)
Trained model file converted to *TensorFlow Lite* file format.
