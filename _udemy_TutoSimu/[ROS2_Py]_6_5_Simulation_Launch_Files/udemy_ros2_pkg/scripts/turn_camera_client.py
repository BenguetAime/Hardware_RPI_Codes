#!/usr/bin/env python3 
import cv2
import rclpy 
from rclpy.node import Node 

from udemy_ros2_pkg.srv import TurnCamera
from cv_bridge import CvBridge 


class TurnCameraClient(Node):
	def __init__(self):
		super().__init__('turn_camera_client_node')
		self.client = self.create_client(TurnCamera, 'turn_camera')
		self.req = TurnCamera.Request()

	def send_request(self, num):
		self.req.degree_turn = float(num)
		self.client.wait_for_service()
		self.future = self.client.call_async(self.req)
		rclpy.spin_until_future_complete(self, self.future)

		self.result = self.future.result()
		return self.result.image

	def display_image(self, image_msg):
		image = CvBridge().imgmsg_to_cv2(image_msg)
		cv2.imshow("Turn Camera Image", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		

def main(args=None):
	rclpy.init()
	client_node = TurnCameraClient()
	print("Turn Camera Client Node Running...")

	try:
		user_input = input("Enter a number in degrees to turn the camera: ")
		res = client_node.send_request(user_input)
		client_node.display_image(res)
	except KeyboardInterrupt:
		print("Terminating Node...")
		client_node.destroy_node()


if __name__ == '__main__':
	main()