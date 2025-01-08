cmake_minimum_required(VERSION 3.8)
project(udemy_ros2_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(ros_ign_gazebo REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
    "srv/OddEvenCheck.srv"
    "srv/TurnCamera.srv"
    "action/Navigate.action"
    DEPENDENCIES 
    sensor_msgs geometry_msgs
)



ament_python_install_package(scripts)

install(PROGRAMS
  scripts/publisher.py 
  scripts/subscriber.py 
  scripts/rpm_pub.py 
  scripts/speed_calc.py 
  scripts/service_server.py 
  scripts/service_client.py 
  scripts/turn_camera_server.py 
  scripts/turn_camera_client.py 
  scripts/action_server.py 
  scripts/action_client.py 
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(DIRECTORY worlds DESTINATION share/${PROJECT_NAME})
install(DIRECTORY models DESTINATION share/${PROJECT_NAME})


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
