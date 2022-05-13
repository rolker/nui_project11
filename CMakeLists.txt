cmake_minimum_required(VERSION 2.8.3)
project(nui_project11)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
)

catkin_python_setup()

catkin_package(
  CATKIN_DEPENDS rospy std_msgs
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

