from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.substitutions import Command


def generate_launch_description():

    robot_description = Command([
        "xacro ",
        PathJoinSubstitution([
            FindPackageShare("line_follower_description"),
            "urdf",
            "robot.urdf.xacro"
        ])
    ])

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py"
            ])
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items()
    )


    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "line_follower_robot",
            "-topic",
            "robot_description"
        ],
        output="screen"
    )


    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {
                "robot_description": robot_description
            }
        ],
        output="screen"
    )


    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])

