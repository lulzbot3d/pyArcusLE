cmake_minimum_required(VERSION 3.20)
cmake_policy(SET CMP0091 NEW)
project(pyarcus)

find_package(protobuf REQUIRED)
find_package(Python REQUIRED)
find_package(arcus REQUIRED)

find_package(standardprojectsettings REQUIRED)
find_package(sipbuildtool REQUIRED)

add_library(pyArcus INTERFACE src/PythonMessage.cpp)
use_threads(pyArcus)

target_include_directories(pyArcus
        INTERFACE
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
        )
target_link_libraries(pyArcus INTERFACE arcus::arcus protobuf::libprotobuf cpython::cpython)
add_sip_module(pyArcus)
install_sip_module(pyArcus)
