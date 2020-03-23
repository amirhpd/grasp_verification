# Description of codes and files

## [model_generator\.ipynb](model_generator.ipynb)
IPython notebook for generating ranges of CNN models. Resulting models are used in the
benchmarking experiment. <br />
Generates CNN models with *Conv2D* layers and with *DepthwiseConv2D* layers.
Receives ranges for hyper-parameters:
* Image size
* No. of filters (only for Conv2D models)
* No. of blocks
* No. of outputs

and generates many CNN models with different 
combinations of these hyper-parameters. 
All models are saved as model files with *.h5* file format.

## [dataset_generator\.py](dataset_generator.py)
Receives the video from camera, splits it
to frames, converts the size to 128x128 pixels, and saves images with a naming
convention into a defined folder. The following terminal command will execute the
code:
```
$python3 dataset_generator.py <className> <framesInterval>
```
Where *className* is a string that specifies the name of the folder in which images
are saved and *framesInterval* is an integer number for setting the video split rate.

## [model_converter\.py](model_converter.py)
Converts CNN model files created by *keras* library (with *.h5* file format) to:
* *TensorFlow Lite* model files (with *.tflite* file format) for *JeVois* Camera.
* *Kendryte* model files (with *.kmodel* file format) for *Sipeed* Camera.

Needs [nncase](https://github.com/kendryte/nncase) library.

## [Inference\.py](Inference.py)
Provides a method to systematically measure the accuracy of the
image classification done by the smart camera while the gripper is operating. <br />
The idea is to use a human evaluator as a reference and compare the result of 
the classification done by the smart camera with the classification done by the human on a 
particular experiment. <br />
The steps are: 
1. Perform a grasping task by the gripper while the smart camera is inferencing.
2. Save the result of classification and the video of the task in a synchronized
manner while the task is operating.
3. After the experiment is finished, play the video for the human evaluator.
4. Save the result of the classification done by the human while the video is
playing.
5. Compare the results and calculate the real-world accuracy.

The inference code is executed while performing the grasping task. The module running
inside the *JeVois* camera publishes the results of the classification on the serial-over-
USB interface. The inference code reads the serial port data and saves them in a file
with *.csv* format. After executing this code, a table and a video are saved on the
host computer.

## [Evaluate\.py](Evaluate.py)
Reads the video and table that are already created by the inference code, 
plays the video for the human evaluator, and saves the result of the classification 
on the table file. <br />
During the video,the human is asked to press keyboard button 
*G* when *grasped* state is shown and press *N* when the state is *not grasped*. 
After playing the video, one column in the
table contains results of the classification by the smart camera and another column
contains human classification results. These two columns are compared and the total
accuracy is calculated. <br />
Assuming that the human results
are always true, the video frames with unequal classification results are the mistakes
of the smart camera. They can be labeled based on the human results and added to
the dataset. A folder called *suggestions* containing the two
classes is created after running the code.

## [camBot\.py](camBot.py)
For the grasp verification experiment with YouBot, instead of a human evaluator, 
the state of the gripper is considered.
During the operation the host computer collects data from two sources of information:
* The status of the robot is stored based on the sent commands.
* The inference results and video received from the smart camera are also stored.

After one cycle is finished, the real-world accuracy is measured by comparing the
inference results from the smart camera with the state of the gripper.
For each cycle a file with *.csv* format containing all the mentioned information 
and the output video recorded by the smart camera are saved on the host computer.
Besides, suggestions for expanding the dataset are generated and stored.

## [sipeed_code\.py](sipeed_code.py)
Code used inside *Sipeed* camera. <br />
Loads a model file with name *model.kmodel*, performs inference, and calculates 
*fps* and *runtime* values.

## Datasets
Datasets collected particularly for this project. <br />
Images are taken with *JeVois* smart camera mounted on the *YouBot* gripper. 
Contains images of *grasped* and *not grasped* situations of different objects and 
with different backgrounds and lightings.
* Classes: grasped, notgrasped 
* Image size: 128x128 
* Augmented: No 

[dataset_1\.zip](dataset_1.zip) : Contains 2134 items for *grasped* class and 2191 items for 
*notgrasped* class. 
Training this dataset will result in **good** accuracy. 
(Tested with fine-tuned MobileNets, single block ResNet) <br />
[dataset_2\.zip](dataset_2.zip) : contains 2376 items for *grasped* class and 2307 items for 
*notgrasped* class. 
Training this dataset will result in **bad** accuracy. 
(Tested with fine-tuned MobileNets, single block ResNet)

## Custom_CNN_Architectures
Details [here](Custom_CNN_Architectures/README.md)

## Fine_tuned_MobileNets
Details [here](Fine_tuned_MobileNets/README.md)

## Single_Block_ResNet
Details [here](Single_Block_ResNet/README.md)
