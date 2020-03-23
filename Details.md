# Description of codes and files
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
This code reads the video and table that are already created by the inference code, 
plays the video for the human evaluator, and saves the result of the classification 
on the table file. During the video,the human is asked to press keyboard button 
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
