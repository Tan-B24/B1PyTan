from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir
from launch_ros.actions import Node
import launch

def generate_launch_description():
    return LaunchDescription([
        # launch the pointcloud to laser scan converter
        Node(
            package='pointcloud_to_laserscan', executable='pointcloud_to_laserscan_node',
            remappings=[('cloud_in', '/b1/rslidar_points'),
                        ('scan', '/b1/rslidar_scans')],
            parameters=[{
                'target_frame': 'b1_rslidar',
                'transform_tolerance': 0.01,
                'min_height': 0.0,
                'max_height': 1.0,
                'angle_min': -1.5708,  # -M_PI/2
                'angle_max': 1.5708,  # M_PI/2
                'angle_increment': 0.0087,  # M_PI/360.0
                'scan_time': 0.3333,
                'range_min': 0.45,
                'range_max': 100.0,
                'use_inf': True,
                'inf_epsilon': 1.0
            }],
            name='pointcloud_to_laserscan'
        ),

        # Launch the front looking D455 camera
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/d455.launch.py'])
        ),

        # Run the B1py calibration TF broadcaster
        Node(
            package='b1py_calib',
            executable='calib_broadcaster',
            name='b1_calib_broadcaster_node'
        ),
        # Launch the LiDAR sensor
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([ThisLaunchFileDir(), '/rslidar.launch.py'])
        ),
        
        # Run the B1py node
         TimerAction(
            period=launch.Duration(5),  # 5 seconds delay
            actions=[
                Node(
                    package='b1py_node',
                    executable='highlevel',
                    name='b1_highlevel_node'
                )
            ]
        ),
    ])
