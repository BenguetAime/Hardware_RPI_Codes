#!/usr/bin/env python3 
import rclpy 
from rclpy.node import Node 

from udemy_ros2_pkg.srv import OddEvenCheck


class OddEvenCheckClient(Node):
	def __init__(self):
		super().__init__('odd_even_client_node')
		self.client = self.create_client(OddEvenCheck, 'odd_even_check')
		self.req = OddEvenCheck.Request()

	def send_request(self, num):
		self.req.number = int(num)
		self.client.wait_for_service()
		self.future = self.client.call_async(self.req)
		rclpy.spin_until_future_complete(self, self.future)

		self.result = self.future.result()
		return self.result 
		

def main(args=None):
	rclpy.init()
	client_node = OddEvenCheckClient()
	print("Odd Even Check Client Server Running...")

	try:
		user_input = input("Enter an integer: ")
		res = client_node.send_request(user_input)
		print("Server returned: " + res.decision)
	except KeyboardInterrupt:
		print("Terminating Node...")
		client_node.destroy_node()


if __name__ == '__main__':
	main()