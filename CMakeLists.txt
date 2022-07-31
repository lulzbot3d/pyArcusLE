cmake_policy(SET CMP0091 NEW)
project(pyarcus)
cmake_minimum_required(VERSION 3.20)
include(cmake/StandardProjectSettings.cmake)

option(BUILD_PYTHON "Build Python bindings for this library" ON)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(cmake/SIPMacros.cmake)

find_package(protobuf 3.17.1 REQUIRED)
find_package(cpython REQUIRED)
find_package(libarcus REQUIRED)

add_library(pyArcus INTERFACE ${CMAKE_SOURCE_DIR}/python/PythonMessage.cpp)
use_threads(pyArcus)

target_include_directories(pyArcus
		INTERFACE
			$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
			$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
		)
target_link_libraries(pyArcus INTERFACE libarcus::libarcus protobuf::libprotobuf cpython::cpython)

add_sip_module(pyArcus)
if (DEFINED Python_SITELIB_LOCAL)
	install_sip_module(pyArcus ${Python_SITELIB_LOCAL})
else()
	install_sip_module(pyArcus)
endif ()
