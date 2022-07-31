cmake_minimum_required(VERSION 3.20)
project(PackageTest)

find_package(pyarcus REQUIRED)
find_package(protobuf 3.17.1 REQUIRED)

configure_file(test.py ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(test.proto ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
