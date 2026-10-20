# Autonomous Surveillance Robot

A hexapod robot project from 2023. A camera feed goes through ROS, objects are detected and logged with a position and timestamp, and a small React Native app lets me watch the log.

## What is in here

| File | What it does |
| --- | --- |
| `Run.py` | ROS node. Subscribes to `/camera/image_raw`, runs ORB-SLAM for mapping, publishes object positions, and writes each detection to SQLite. |
| `hexapod_control.py` | Runs on the Raspberry Pi. Takes a target image through a small Tkinter window, matches it with ORB features and a face cascade, and drives the legs over serial. |
| `hexapod_arduino.ino` | Arduino sketch for the leg servos. |
| `Monitoring Application.js` | React Native screen that reads the detection log. |
| `surveillance_data.db` | Sample SQLite database with three example rows (`timestamp`, `object_class`, x/y/z). |

## How it works

1. The camera publishes frames on ROS.
2. `Run.py` converts them with `cv_bridge`, updates the map and records any detected object in the `surveillance_data` table.
3. The monitoring app reads that table so I can see what the robot saw and where.

## Running it

You need Python 3, ROS (I used Melodic), OpenCV and a camera topic. Then:

```bash
rosbridge
python Run.py
```

The database is created on first run if it does not exist.

## Notes

This was a prototype. The ORB-SLAM call and the hardware pins are specific to my build, so expect to adjust them for yours.
