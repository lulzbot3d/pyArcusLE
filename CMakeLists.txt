cmake_policy(SET CMP0091 NEW)
project(pyarcusle)
cmake_minimum_required(VERSION 3.20)

# Set LC_LIBRARY_PATH variable to ensure CMake can actually use the CPython library
set(ENV{LD_LIBRARY_PATH} "${CMAKE_LIBRARY_PATH}:${LD_LIBRARY_PATH}")
find_package(Python3 REQUIRED)
find_package(protobuf REQUIRED)
find_package(arcusle REQUIRED)

find_package(standardprojectsettings REQUIRED)
find_package(sipbuildtool REQUIRED)

add_library(pyArcus INTERFACE src/PythonMessage.cpp)
use_threads(pyArcus)

target_include_directories(pyArcus
        INTERFACE
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
        )
target_link_libraries(pyArcus INTERFACE arcusle::arcusle protobuf::libprotobuf cpython::cpython)
add_sip_module(pyArcus)
install_sip_module(pyArcus)

