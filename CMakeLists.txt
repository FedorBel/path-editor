cmake_minimum_required(VERSION 3.0.0)
project(path_editor VERSION 0.1.0 LANGUAGES C CXX)

include(CTest)
enable_testing()

add_library(path_editor path_editor.cpp)


add_library(hack SHARED hack.c)

target_include_directories(hack
    PRIVATE
    /usr/include/python3.8/
)


find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

target_link_libraries(hack INTERFACE
  Python3::Python
  Python3::Module
)


set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
