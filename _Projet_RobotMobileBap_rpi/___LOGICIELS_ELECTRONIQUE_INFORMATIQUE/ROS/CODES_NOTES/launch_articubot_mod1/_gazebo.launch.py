import os

from ament_index_python.packages import get_package_share_directory
from pathlib import Path 

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument,ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():
    # Include the robot_state_publisher launch file, provided by our own package. 
    # Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='articubot_one' #<--- CHANGE ME
    gazebo_pkg_name = 'ros_ign_gazebo' # 'gazebo_ros' pour gazebo classic
    ################ perso : useful cmds 
    pkg_path = get_package_share_directory(package_name)
    pkg_gazebo_ros = get_package_share_directory(gazebo_pkg_name)
    pkg_gazebo_worlds = get_package_share_directory(gazebo_pkg_name)# sinon personnaliser 
    simulation_world_file_path = os.path.join(pkg_gazebo_worlds, 'worlds','personalized_world.sdf')
    simulation_models_path = Path(pkg_path, "models").as_posix()
    ## Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'ign_gazebo.launch.py'),
        ),
        launch_arguments=[('pause', 'true')],  # Pass the pause argument here
    )
    
    ##
    simulation_gazebo = ExecuteProcess(
    cmd=['ign', 'gazebo','--render-engine','ogre','-r', simulation_world_file_path],
    output='screen')
    
    ##urdf 1
    urdf_model_path = os.path.join(pkg_path, 'urdf', 'Ros2_RobotBipede.urdf')
    with open(urdf_model_path, 'r') as infp:
        robot_desc = infp.read()
    params = {'robot_description': robot_desc}
    ##urdf 2 rajouter "params" comme il faut, dans joint state pub node, robot state pub node 
    ##urdf 3 : rajouter ce qui suit dans le return LaunchDescription
    launch.actions.DeclareLaunchArgument(
    name='model',
    default_value=urdf_model_path,
    description='Path to the URDF model file')
    
    ## ! ! ! Rajouter dans le return launchDescription :
    SetEnvironmentVariable(
            name="IGN_GAZEBO_RESOURCE_PATH",
            value=simulation_models_path
    )
    # rajouter dans le return LaunchDescription : gazebo, simulation_gazebo(si on souhaite utiliser 
    # ce monde personnalisé; sinon laisser uniquement "gazebo")
    ################ perso : useful cmds 




    ################
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('ros_ign_gazebo'), 'launch', 'ign_gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'package_name'],
                        output='screen')



    # Launch them all!
    return LaunchDescription([
            SetEnvironmentVariable(
            name="IGN_GAZEBO_RESOURCE_PATH",
            value=simulation_models_path
        ),
        rsp,
        gazebo,
        simulation_gazebo,
        spawn_entity,
    ])

