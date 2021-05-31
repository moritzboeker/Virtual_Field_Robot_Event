#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 05:26:51 2021

@author: fre
"""

#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose, Point, Quaternion
from gazebo_msgs.srv import GetModelState
from urdf_parser_py.urdf import URDF

counter = 0
robot_name = ''

def callback(data):
    global counter
    global robot_name
    
    ms = gms(robot_name, "")
    ms.pose.position.z += 1
        
    name = 'marker_%d' %counter
    counter += 1
    cont = create_marker(name, data.data)
    
    a = spawn_model(name, cont, "marker", ms.pose,"world")
    print(a)
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("fre_detections", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    
def create_marker(name, kind):


    cont = "<sdf version='1.6'>  \
<model name='%s'> \
    <static>true</static> \
  <pose frame=''>0 0 0 0 0 0</pose> \
  <link name='marker_link'> \
    <visual name='visual'> \
      <geometry> \
        <cylinder> \
          <radius>0.375</radius> \
          <length>1</length> \
        </cylinder> \
      </geometry> \
      <material> " %(name)
      
    if kind == 'weed':
        cont += "<ambient>1.0 0.0 0.0 0.4</ambient> \
        <diffuse>1.0 0.0 0.0 0.4</diffuse> \
        <specular>1.0 0.0 0.0 0.4</specular> \
        <emissive>0.0 0.0 0.0 0.0</emissive>"
    
    elif kind == 'litter':
        cont += "<ambient>0.0 0.0 1.0 0.4</ambient> \
        <diffuse>0.0 0.0 1.0 0.4</diffuse> \
        <specular>0.0 0.0 1.0 0.4</specular> \
        <emissive>0.0 0.0 0.0 0.0</emissive>"
    
    cont += "</material> \
    </visual> \
    <self_collide>0</self_collide> \
    <enable_wind>0</enable_wind> \
    <kinematic>0</kinematic> \
  </link> \
</model> \
    </sdf>" 

    return cont



if __name__ == '__main__':
    rospy.wait_for_service("gazebo/spawn_sdf_model")
    rospy.wait_for_service('/gazebo/get_model_state')
    gms = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
    robot_name = URDF.from_parameter_server().name
    spawn_model  = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
    
    listener()