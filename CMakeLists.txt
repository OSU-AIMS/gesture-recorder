cmake_minimum_required(VERSION 3.0.2)
project(gesture_recorder)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  )

catkin_package()

install(DIRECTORY config launch scripts
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
