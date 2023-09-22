# Autonomous Surveillance Robot 🤖

This repository contains code for an autonomous surveillance robot. The robot uses SLAM (Simultaneous Localization and Mapping) to navigate its environment and object detection to identify and track objects of interest. The robot's data is stored in a SQLite3 database, which can be monitored using the React Native monitoring application.

## Getting started

### Prerequisites:

Python 3
ROS
React Native
Instructions:

Clone this repository to your computer.

Install the required dependencies:

Python 3: pip install python3
ROS: sudo apt install ros-melodic-desktop-full
React Native: npm install -g react-native-cli
Create a SQLite3 database named surveillance_data.db. You can do this using the following command:
sqlite3 surveillance_data.db
Start the ROSBridge server:
rosbridge
Run the Python autonomous surveillance robot code:
python surveillance_robot.py
Run the React Native monitoring app:

cd monitoring-app
npm start
Usage

The autonomous surveillance robot will start navigating its environment and detecting objects. You can monitor the robot's data in the React Native monitoring application.

Features🤖

SLAM navigation🗺️
Object detection👁️
SQLite3 database storage💾
React Native monitoring application📱

    

User-friendly instructions

To get started with the autonomous surveillance robot:

Clone this repository to your computer.
Install the required dependencies.
Create a SQLite3 database.
Start the ROSBridge server.
Run the Python autonomous surveillance robot code.
Run the React Native monitoring app.
Once the robot is running, you can monitor its data in the React Native monitoring application. The application will display the robot's map, object positions, and surveillance data.

Troubleshooting

If you are having trouble running the autonomous surveillance robot, please refer to the following troubleshooting tips:

Make sure that you have installed all of the required dependencies.
Make sure that the ROSBridge server is running.
Make sure that the SQLite3 database exists.
Check the Python autonomous surveillance robot code for any errors.
Check the React Native monitoring app code for any errors.
If you are still having trouble, please feel free to contact me for assistance.
