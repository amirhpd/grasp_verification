# Custom CNN Architectures
Two architectures from model range generation are trained and used for the grasp 
verification task. These models are
constructed from simple CNN blocks, they are small and naive when compared with
*MobileNets* or *ResNet* architectures. Yet the comparison of the results when used
in grasp verification would illustrate how complicated the model should be for this
specific task.

## [conv2d\.ipynb](conv2d.ipynb)
IPython notebook for generating and training custom CNN architecture with *Conv2D* layers.
The resulting model files are used for the grasp verification tasks.
This code 
* generates a simple CNN model
* trains the model
* prints confusion matrix
* saves the trained model as *.h5* and *.tflite* files 

## [conv2d\.h5](conv2d.h5)
Trained model file from *keras* library. This file contains the detais and 
can be loaded again by *keras* library.

## [conv2d\.tflite](conv2d.tflite)
Trained model file converted to *TensorFlow Lite* file format.

## [depthwiseconv2d\.ipynb](depthwiseconv2d.ipynb)
IPython notebook for generating and training custom CNN architecture with 
*depthwiseconv2D* layers.
The resulting model files are used for the grasp verification tasks.
This code 
* generates a simple CNN model
* trains the model
* prints confusion matrix
* saves the trained model as *.h5* and *.tflite* files 

## [depthwiseconv2d\.h5](depthwiseconv2d.h5)
Trained model file from *keras* library. This file contains the detais and 
can be loaded again by *keras* library.

## [depthwiseconv2d\.tflite](depthwiseconv2d.tflite)
Trained model file converted to *TensorFlow Lite* file format.
