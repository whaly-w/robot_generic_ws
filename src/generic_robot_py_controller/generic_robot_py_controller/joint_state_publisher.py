import rclpy
from generic_robot_py_controller.publisher_classes import VariablePublisher

import numpy as np
from sensor_msgs.msg import JointState

class JointStatePublisher(VariablePublisher):
    def __init__(self):
        super().__init__('joint_state_publisher', '/joint_command', JointState)

        self.declare_parameter('vel_limit', 2.0)
        self._vel_limit = float(self.get_parameter('vel_limit').value)

    
    def publish_cmd(self, cmd):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self._joint_names
        msg.position = np.zeros(self._joint_num).tolist()
        msg.velocity = (np.ones(self._joint_num) * self._vel_limit).tolist()
        
        for i, joint_name in enumerate(self._joint_names):
            for joint_no, joint_value in cmd.items():
                if i == joint_no:
                    msg.position[i] = joint_value
                    self.get_logger().info(f'{joint_name} command to {joint_value} rad')

        self._joint_pub.publish(msg)
        self.get_logger().info(f'\n\n')

    def timer_callback_random(self):
        ran = np.random.uniform(self.mn, self.mx, self._joint_num)
        
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self._joint_names
        # msg.position = ran.tolist()
        msg.position = self._default_pos
        msg.velocity = (np.ones(self._joint_num) * self._vel_limit).tolist()
        msg.effort = np.zeros(self._joint_num).tolist()
        
        self._joint_pub.publish(msg)
        # self.get_logger().info(f'Published >> {ran}')
        self.get_logger().info(f'Published >> {msg.position}')
        
    
def main(args= None):
    rclpy.init(args= args)
    
    node = JointStatePublisher()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()