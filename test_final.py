#!/usr/bin/python
'''
Authors:
Khaled Hassan, 
Forrest Voight
Jacob Panikulam
'''

# modified by Paul Chojecki (11-3-2015)
# portions of code taken from andrewdai.co/xbox-controller-ros.html
# portions of code taken from wiki.ros.org/rospy_tutorials/Tutorials/WritingPublisherSubscriber

from __future__ import division
import rospy
import numpy as np
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Wrench, WrenchStamped, Vector3
from std_msgs.msg import String

rospy.init_node('joystick_command')
pub = rospy.Publisher('wrench', WrenchStamped, queue_size=1)
is_classic_ctrl = True

def callback(data):
	global is_classic_ctrl

	wrench = WrenchStamped()

	if data.buttons[0]: # 'A' button
		is_classic_ctrl = True
	elif data.buttons[1]: # 'B' button
		is_classic_ctrl = False
	
	if is_classic_ctrl:
		linear_x = data.axes[1] * max_x_force
		linear_y = data.axes[0] * max_y_force
		angular_z = data.axes[2] * max_z_torque
	else:
		linear_x = data.axes[1] * .5 * max_x_force + data.axes[3] * .5 * max_x_force
		linear_y = data.axes[0] * max_y_force * .5 + data.axes[2] * max_y_force * .5
		angular_z = data.axes[3] * max_z_torque * .5 - .5 * max_z_torque * data.axes[1]
	
	wrench.wrench.force.x = linear_x
	wrench.wrench.force.y = linear_y
	wrench.wrench.force.z = 0
    
	wrench.wrench.torque.x = 0
	wrench.wrench.torque.y = 0
	wrench.wrench.torque.z = angular_z
	print wrench.wrench.force.x

	pub.publish(wrench)

max_x_force = 75
max_y_force = 75
max_z_torque = 75

def start():
	rospy.Subscriber("/joy", Joy, callback)
	rospy.spin()

if __name__ == '__main__':
	start()
