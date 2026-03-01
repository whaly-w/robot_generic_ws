import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/whaly/robot_generic_ws/install/generic_robot_py_controller'
