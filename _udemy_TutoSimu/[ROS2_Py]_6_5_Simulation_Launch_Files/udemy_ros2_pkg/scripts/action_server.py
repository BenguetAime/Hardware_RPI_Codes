#!/usr/bin/env python3
import math
import rclpy 
from rclpy.node import Node 

from rclpy.action import ActionServer
from geometry_msgs.msg import Point
from udemy_ros2_pkg.action import Navigate 

DISTANCE_THRESHOLD = 0.125

class NavigateActionServer(Node):
	def __init__(self):
		super().__init__("action_server_node")
		self._action_server = ActionServer(self, Navigate, 'navigate', self.navigate_callback)
		self.sub = self.create_subscription(Point, 'robot_position', self.update_robot_position, 1)
		self.robot_current_position = None 

	def navigate_callback(self, goal_handle):
		print("Received Goal")
		start_time = self.get_clock().now().to_msg().sec 
		robot_goal_point = [goal_handle.request.goal_point.x, 
							goal_handle.request.goal_point.y,
							goal_handle.request.goal_point.z]

		print("Goal Point: " + str(robot_goal_point))

		while self.robot_current_position == None:
			print("Robot Point Not Detected")
			rclpy.spin_once(self, timeout_sec=3)

		distance_to_goal = math.dist(self.robot_current_position, robot_goal_point)
		feedback_msg = Navigate.Feedback()

		while distance_to_goal > DISTANCE_THRESHOLD:
			distance_to_goal = math.dist(self.robot_current_position, robot_goal_point)
			feedback_msg.distance_to_point = distance_to_goal
			goal_handle.publish_feedback(feedback_msg)
			rclpy.spin_once(self, timeout_sec=1)

		goal_handle.succeed()
		result = Navigate.Result()
		result.elapsed_time = float(self.get_clock().now().to_msg().sec - start_time)

		return result


	def update_robot_position(self, point):
		self.robot_current_position = [point.x, point.y, point.z]


def main(args=None):
	rclpy.init()
	action_server_node = NavigateActionServer()
	print("Action Server Running...")

	try:
		while rclpy.ok():
			rclpy.spin_once(action_server_node)
	except KeyboardInterrupt:
		print("Terminating Node...")
		action_server_node._action_server.destroy()
		action_server_node.destroy_node()


if __name__ == '__main__':
	main()