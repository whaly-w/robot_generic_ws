from setuptools import find_packages, setup

package_name = 'generic_robot_py_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='whaly',
    maintainer_email='16210888+whxlz@user.noreply.gitee.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'joint_state_publisher=generic_robot_py_controller.joint_state_publisher:main',
            'robot_position_controller_publisher=generic_robot_py_controller.robot_position_controller_publisher:main',
            
        ],
    },
)
