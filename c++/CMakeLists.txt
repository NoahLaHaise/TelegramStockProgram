cmake_minimum_required(VERSION 3.20)
project(DataAnalysisEngine)

get_filename_component(PARENT_DIR ${CMAKE_CURRENT_SOURCE_DIR} DIRECTORY)
add_definitions(-DPROJECT_ROOT_DIR="${PARENT_DIR}")

set(CMAKE_CXX_STANDARD 17)

add_executable(DataAnalysisEngine DataAnalysisEngine.cpp)