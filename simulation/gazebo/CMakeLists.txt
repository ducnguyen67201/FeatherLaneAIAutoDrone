cmake_minimum_required(VERSION 3.16)
project(featherlane_gazebo_bridge LANGUAGES CXX)

# Build only the official actuator/state bridge needed by this headless scene.
# Camera, streaming and parachute plugins are separate learning scope.
set(ARDUPILOT_GAZEBO_SOURCE "" CACHE PATH "Pinned official ardupilot_gazebo checkout")
if(NOT EXISTS "${ARDUPILOT_GAZEBO_SOURCE}/src/ArduPilotPlugin.cc")
    message(FATAL_ERROR "Set ARDUPILOT_GAZEBO_SOURCE to the pinned plugin checkout")
endif()

find_package(gz-sim8 REQUIRED)
find_path(RAPIDJSON_INCLUDE_DIR rapidjson/document.h REQUIRED)

add_library(ArduPilotPlugin SHARED
    "${ARDUPILOT_GAZEBO_SOURCE}/src/ArduPilotPlugin.cc"
    "${ARDUPILOT_GAZEBO_SOURCE}/src/SocketUDP.cc"
    "${ARDUPILOT_GAZEBO_SOURCE}/src/Util.cc"
)
target_compile_features(ArduPilotPlugin PRIVATE cxx_std_17)
target_include_directories(ArduPilotPlugin PRIVATE
    "${ARDUPILOT_GAZEBO_SOURCE}/include"
    "${RAPIDJSON_INCLUDE_DIR}"
)
target_link_libraries(ArduPilotPlugin PRIVATE gz-sim8::gz-sim8)
target_compile_options(ArduPilotPlugin PRIVATE -Wall -Wextra)
