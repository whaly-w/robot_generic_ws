import rclpy
from rclpy.node import Node

import yaml
import numpy as np

class VariablePublisher(Node):
    def __init__(self, node_name, default_topic, msg_type):
        super().__init__(node_name)
        
        self.declare_parameter('topic', default_topic)
        self.declare_parameter('config_path', '/config.yaml')
        self.declare_parameter('range', '-1_1')
        self.declare_parameter('delay_time', 1.0)
        self.declare_parameter('random_value', False)
        self.declare_parameter('default_pos', False)
        
        self.mn, self.mx = [int(i) for i in self.get_parameter('range').value.split('_')]
        
        self._delay_time = float(self.get_parameter('delay_time').value)
        config_path = self.get_parameter('config_path').value
        with open(config_path) as file:
            data = yaml.safe_load(file)
        self._robot_name = list(data.keys())[0]
        self._joint_names = data[self._robot_name]['joint_names']
        try:
            self._joint_names += data[self._robot_name]['unused_joints']
            self.unused_joint_num = len(data[self._robot_name]['unused_joints'])
        except:
            self.unused_joint_num = 0
        self._joint_num = len(self._joint_names)

        try:
            self._default_pos = np.array(data[self._robot_name]['default_dof_pos'], dtype= np.float64).tolist()
        except KeyError:
            self._default_pos = np.zeros(self._joint_num).tolist()
        
        self._topic = self.get_parameter('topic').value
        self._joint_pub = self.create_publisher(msg_type, self._topic, 500)
        
        if self.get_parameter('random_value').value:
            self._timer = self.create_timer(self._delay_time, self.timer_callback_random)
        else:
            self._timer = self.create_timer(self._delay_time, self.timer_callback)

        self.joint_set = []
        for i, joint_name in enumerate(self._joint_names):
            try:
                sp = joint_name.split('_')
                self.joint_set.append((sp[2] + ' ' + sp[3] + ' ' + sp[1], i, joint_name))
            except:
                self.joint_set.append((joint_name.strip('Joint_'), i, joint_name))
        self.joint_set.sort()

        print(f'Initialized {node_name} at {self._topic} for [{self._robot_name}] with {self._joint_num} joints')

    def timer_callback(self):
        msg = '\n'

        msg_list = [f'{i}: {joint_name}' for _, i, joint_name in self.joint_set]
        msg += '\n'.join(msg_list)
        self.get_logger().info(msg)

        cmd = {}
        while (_in:=input('\n>> Joint No. | Value (rad)\nEnter: ')) != 'q':
            print(_in)
            try:
                _in = _in.split()
                index = int(_in[0])
                
                if index >= self._joint_num:
                    print('Index out of range')
                    continue
                elif index < 0:
                    print('Command to default position')
                    cmd = {i: self._default_pos[i] for i in range(self._joint_num - self.unused_joint_num)}
                    for i in range(self.unused_joint_num):
                        cmd[self._joint_num - self.unused_joint_num + i] = 0.0
                    break
                cmd[index] = float(_in[1])
            except:
                print('input error')
                continue
            print('CMD:', cmd)

        self.publish_cmd(cmd)

    def publish_cmd(self, cmd):
        raise NotImplementedError

    def timer_callback_random(self):
        raise NotImplementedError
