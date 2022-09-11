Installation
===========

Clone this project into a local repository. Then, install requirements with
`pip install requirements.txt`

If you have python3 installed and set up correctly, you should be able to run `python main.py` to run the software. Otherwise, double check your python installation.

Software Overview
========

![Drawing paths in the software](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/field.png?raw=true)
The heart of this software is drawing paths onto the vex field. In edit mode, left click to add new points, hover over an object and press 'X' to delete. You can also zoom and pan around the field for more precision.

By default, every point is set to "smooth", where the robot will follow some sort of curve about that point. To toggle this to a sharp point turn, right click the point.

![Simulation mode](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/simulate.png?raw=true)
To switch to simulation mode, click on the corresponding button on the top right corner of the screen. The goal of this mode is to be able to simulate different types of path following algorithms like Pure Pursuit and Stanley, and fine tune parameters. As shown in the image, there would be buttons to be able to switch between different algorithms, and a set of sliders associated with each algorithm corresponding to a number of tunable parameters.

![Robot mode](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/robot.png?raw=true)
Robot mode's interface is somewhat similar to simulation mode, except, instead of running simulations, we're able to export this data and actually run the path on the robot. The tunable parameters for each algorithm is purposefully distinct from those of simulation mode, so you can tune your real robot differently to the robot model, which is unavoidable due to the imperfections of the robot simulation. This mode would also allow you to import the robot's position data over time after the run, so we can get visual feedback on how the robot's actual path differed from what what was desired.

![Odometry mode](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/odom.png?raw=true)
Odometry mode is for obtaining real-time odometry data from the robot through serial. This mode displays the robot's estimated position in real time, as well as logging individual encoders and any other sensors that might be related to localization.
