import rclpy
from rclpy.node import Node

import yaml
import numpy as np
from sensor_msgs.msg import JointState

class JointStatePublisher(Node):
    def __init__(self):
        super().__init__('joint_state_publisher')
        
        self.declare_parameter('topic', 'joint_command')
        self.declare_parameter('config_path', '/config.yaml')
        self.declare_parameter('range', '-1_1')
        self.declare_parameter('delay_time', 1.0)
        self.declare_parameter('random_value', False)
        
        self.mn, self.mx = [int(i) for i in self.get_parameter('range').value.split('_')]
        # self.mn, self.mx = [-1, 1]
        # print(self.mx, self.mn)
        
        self._delay_time = float(self.get_parameter('delay_time').value)
        config_path = self.get_parameter('config_path').value
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self._robot_name = list(data.keys())[0]
        self._joint_names = data[self._robot_name]['joint_names']
        self._joint_num = len(self._joint_names)
        
        self._topic = f"/{self._robot_name}/{self.get_parameter('topic').value}"
        self._joint_pub = self.create_publisher(JointState, self._topic, 500)
        
        # print(self.get_parameter('random_value').value)
        if self.get_parameter('random_value').value:
            self._timer = self.create_timer(self._delay_time, self.timer_callback_random)
        else:
            self._timer = self.create_timer(self._delay_time, self.timer_callback)
        
        print(f'Initialized joint command at {self._topic} for [{self._robot_name}] with {self._joint_num} joints')
    
    def timer_callback(self):
        msg = '\n'
        msg_list = [f'{i}: {joint_name}' for i, joint_name in enumerate(self._joint_names)]
        msg += '\n'.join(msg_list)
        self.get_logger().info(msg)


        cmd = {}
        while (_in:=input('\n>> Joint No. | Value (rad)\nEnter: ')) != 'q':
            try:
                _in = _in.split()
                cmd[int(_in[0])] = float(_in[1])
            except:
                print('input error')
                continue
            print('CMD:', cmd)

        msg = JointState()
        msg.name = self._joint_names
        msg.position = np.zeros(self._joint_num).tolist()
        msg.velocity = (np.ones(self._joint_num) * 2.0).tolist()
        

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
        
        msg.name = self._joint_names
        msg.position = ran.tolist()
        
        self._joint_pub.publish(msg)
        self.get_logger().info(f'Published >> {ran}')
        
    
    
def main(args= None):
    rclpy.init(args= args)
    
    node = JointStatePublisher()
    rclpy.spin(node)
    
    node.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()
        