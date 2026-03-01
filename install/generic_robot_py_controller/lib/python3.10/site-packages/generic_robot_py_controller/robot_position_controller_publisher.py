import rclpy
from rclpy.node import Node

import yaml
import numpy as np
from std_msgs.msg import Float64MultiArray

class RobotPositionControllerPublisher(Node):
    def __init__(self):
        super().__init__('robot_position_controller_publisher')
        
        self.declare_parameter('topic', '/robot_position_controller/commands')
        self.declare_parameter('config_path', '/config.yaml')
        self.declare_parameter('range', '-1_1')
        self.declare_parameter('delay_time', 1.0)
        self.declare_parameter('random_value', True)
        
        self.mn, self.mx = [int(i) for i in self.get_parameter('range').value.split('_')]
        
        self._delay_time = float(self.get_parameter('delay_time').value)
        config_path = self.get_parameter('config_path').value
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self._robot_name = list(data.keys())[0]
        self._joint_names = data[self._robot_name]['joint_names']
        self._joint_num = len(self._joint_names)
        
        self._topic = self.get_parameter('topic').value
        self._joint_pub = self.create_publisher(Float64MultiArray, self._topic, 500)
        
        if self.get_parameter('random_value').value:
            self._timer = self.create_timer(self._delay_time, self.timer_callback_random)
        else:
            self._timer = self.create_timer(self._delay_time, self.timer_callback)
        
        print(f'Initialized robot position controller publisher at {self._topic} for [{self._robot_name}] with {self._joint_num} joints')
    
    def timer_callback(self):
        msg = '\n'
        msg_list = [f'{i}: {joint_name}' for i, joint_name in enumerate(self._joint_names)]
        msg += '\n'.join(msg_list)
        self.get_logger().info(msg)

        _in = input('\n>> Joint No. | Value (rad)\nEnter: ').split()
        joint_no = int(_in[0])
        joint_value = float(_in[1])

        cmd = Float64MultiArray()
        cmd.data = np.zeros(self._joint_num).tolist()

        for i, joint_name in enumerate(self._joint_names):
            if i == joint_no:
                cmd.data[i] = joint_value
                self.get_logger().info(f'{joint_name} command to {joint_value} rad')

        self._joint_pub.publish(cmd)

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
