import rclpy
from generic_robot_py_controller.publisher_classes import VariablePublisher

import numpy as np
from std_msgs.msg import Float64MultiArray

class RobotPositionControllerPublisher(VariablePublisher):
    def __init__(self):
        super().__init__('robot_position_controller_publisher', '/robot_position_controller/commands', Float64MultiArray)
        
    def publish_cmd(self, cmd):
        msg = Float64MultiArray()
        msg.data = np.zeros(self._joint_num).tolist()

        for i, joint_name in enumerate(self._joint_names):
            for joint_no, joint_value in cmd.items():
                if i == joint_no:
                    msg.data[i] = joint_value
                    self.get_logger().info(f'{joint_name} command to {joint_value} rad')

        self._joint_pub.publish(msg)
        self.get_logger().info(f'\n\n')

    def timer_callback_random(self):
        ran = np.random.uniform(self.mn, self.mx, self._joint_num)
        
        msg = Float64MultiArray()
        msg.data = ran.tolist()
        
        self._joint_pub.publish(msg)
        self.get_logger().info(f'Published >> {ran}')
        
    
def main(args= None):
    rclpy.init(args= args)
    
    node = RobotPositionControllerPublisher()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
