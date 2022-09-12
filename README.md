Installation
===========

Clone this project into a local repository. Then, install requirements with
`pip install -r requirements.txt`

If you have python3 installed and set up correctly, you should be able to run `python main.py` to run the software. Otherwise, double check your python installation.

Software Overview
========

## Edit Mode

![Drawing paths in the software](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/field.png?raw=true)
The heart of this software is drawing paths onto the vex field. In edit mode, left click to add new points, hover over an object and press X to delete. You can also zoom and pan around the field for more precision.

By default, every point is set to "smooth", where the robot will follow some sort of curve about that point. To toggle this to a sharp point turn, right click the point.

## Simulation Mode

![Simulation mode](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/simulate.png?raw=true)
To switch to simulation mode, click on the corresponding button on the top right corner of the screen. The goal of this mode is to be able to simulate different types of path following algorithms like Pure Pursuit and Stanley, and fine tune parameters. As shown in the image, there would be buttons to be able to switch between different algorithms, and a set of sliders associated with each algorithm corresponding to a number of tunable parameters.

## Robot Mode

![Robot mode](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/robot.png?raw=true)
Robot mode's interface is somewhat similar to simulation mode, except, instead of running simulations, we're able to export this data and actually run the path on the robot. The tunable parameters for each algorithm is purposefully distinct from those of simulation mode, so you can tune your real robot differently to the robot model, which is unavoidable due to the imperfections of the robot simulation. This mode would also allow you to import the robot's position data over time after the run, so we can get visual feedback on how the robot's actual path differed from what what was desired.

## Odometry Mode
![Odometry mode](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/odom.png?raw=true)
Odometry mode is for obtaining real-time odometry data from the robot through serial. This mode displays the robot's estimated position in real time, as well as logging individual encoders and any other sensors that might be related to localization.


Code Structure
=============
![Class hierarchy](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/classes.png?raw=true)
A hierarchy of all the classes in this software so far. Try to absorb as much as you can, but it will make more sense with some context below.

## The overarching game loop

The game loop takes place in main() inside main.py. It can be roughly decomposed to the following steps for each frame:
1. Poll keyboard and mouse input, and store the data in the singleton UserInput
2. Loop through each game object with a global mouse-object interaction system, and store state in the singleton SoftwareState
3. Update the various objects and react to the actions of the mouse
4. Draw everything

Throughout this game loop, there are various singletons that store some sort of state, and get passed around to many functions.
- **FieldTransform** -> storing zooming and panning of the game field
- **FieldSurface** -> The vex field object, which is draggable and thus modifies FieldTransform
- **UserInput** -> Storing keyboard and mouse state, as well as some other I/O like quitting and dragging files
- **FullPath** -> Storing all the data regarding the full path (path points, control points, segments, and waypoints)
- **ButtonCollection** -> Storing all the buttons in the software

For more information, go through each individual file for documentation in further detail.

## The global mouse-object interaction system

This software features a centralized way of handling hovering, clicking, and dragging different types of objects with differing behaviors globally.

![Draggable and Clickable interfaces implement Hoverable](https://github.com/AnselChang/PathGeneration/blob/main/Images/Demo/mouseInterfaceClasses.png?raw=true)

Every object that can be hovered, dragged, or clicked implemenets one of these three interfaces. The key function `getHoverables()` in MouseInteraction.py, using the python generator pattern, returns an iterator for every single hoverable object in the order of checking collision with the mouse. This is iterated through in the function 'handleHoverables()' of the same file, whichk when detecting a mouse colliding with a object, calls that abstract Hoverable and/or Draggable/Clickable functions that would be implemented in the object. This way, each object can be coded to react in its own way to mouse inputs.

I would heavily recommend looking through both functions to get a concrete grasp of how this works. Thus, whenever it is desired to create an object that can be dragged or clicked, all it takes is implementing one of the interfaces and then adding it to the `getHoverables()` generator.

## Converting between screen and field reference frames

Many objects like the different path points are stored in relation to the VEX field, meaning that, as the field pans and zooms, the path points move with the field. Instead of having to manually call functions to convert back and forth all of the time, we use the PointRef class found in ReferenceFrame.py to store points that can be interpreted in both reference frames. Internally, this stores the point in the field reference frame and converts to the screen reference frame when needed, but objects that use PointRefs don't need to worry about this and can seamlessly store and get the position of the point from both reference frames. Note that each pointRef stores a reference to the singleton FieldTransform in order to internally convert between the two reference frames.

PointRef is used everywhere. All the locations of the PathPoints, waypoints, etc. are stored as PointRefs, so that all the path generation math can happen in the field reference frame, but they can interact with the mouse and be drawn on the screen using the screen reference frame.

ControlPoints are tied to PathPoints, and so to define their location relative to PathPoints, I created a VectorRef class, which similarly can be interpreted with both reference frames. In addition, PointRefs and VectorRefs can be added, subtracted, etc. to create easy-to-use vector math. Refer to ReferenceFrame.py for more details.

## Robot simulation and path following algorithms
