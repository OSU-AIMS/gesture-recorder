# Gesture Recorder

![Build Status: Github Actions - Melodic](https://github.com/osu-aims/gesture-recorder/actions/workflows/ci_focal_melodic.yml/badge.svg)
[![license - apache 2.0](https://img.shields.io/:license-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)


Support tool for the Autonomous Gesture Interpretation project. 


### Usage
Primary usage is via two launch files.

| Launch File | Optional Parameters | Description |
| ----------- | ------------------- | ----------- |
| gesture_record.launch | record_bag:=*True/False* <br>save_folder:=*"String Folder Name"* <br>save_images:=*True/False* | Tool for recording gestures using a camera. |
| tool_rosbagextraction.launch | file2extract:=*"FilePath"* <br>topic2extract:=*"/your/topic/name"* | Tool for extracting individual frames from existing ROSBag files. |

** A third launch file exists, but it is a Tier2 launch file designed to support the above Tier1 files. 
