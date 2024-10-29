# ROS2 Python 예제 코드 (Odometry 메시지 구독)
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class PositionPublisher(Node):
    def __init__(self):
        super().__init__('position_publisher')
        self.subscription = self.create_subscription(Odometry, '/odom', self.listener_callback, 10)
        
    def listener_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        print(f"Current Position: x={x}, y={y}")
        # WebSocket 또는 REST API를 통해 UI에 전송

rclpy.init()
position_publisher = PositionPublisher()
rclpy.spin(position_publisher)
rclpy.shutdown()
