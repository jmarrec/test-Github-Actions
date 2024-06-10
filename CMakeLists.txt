cmake_minimum_required(VERSION 3.17)

# Use ccache if available, has to be before "project()"
find_program(CCACHE_PROGRAM NAMES ccache sccache)
if(CCACHE_PROGRAM)
  # Support: Unix Makefiles and Ninja only
  message(STATUS "Using CCACHE")
  # RULE_LAUNCH_COMPILE is an internal variable and makes RC compilation fail on windows, hence why we use the C/CXX COMPILER_LAUNCHER instead
  message(STATUS "${CCACHE_PROGRAM} found and enabled")
  set(CMAKE_CXX_COMPILER_LAUNCHER ${CCACHE_PROGRAM} CACHE FILEPATH "CXX compiler cache used")
  set(CMAKE_C_COMPILER_LAUNCHER ${CCACHE_PROGRAM} CACHE FILEPATH "C compiler cache used")
endif()

cmake_policy(SET CMP0048 NEW) # handling project_version_* variables

project(TestPython VERSION 0.0.1)

if(UNIX AND NOT APPLE)
  set(CMAKE_INSTALL_RPATH "$ORIGIN")
endif()

set(Python_REQUIRED_VERSION "" CACHE STRING "The specific Python version you want to link to (Optional)")
set(Python_ROOT_DIR "" CACHE PATH "The path to the root installation of your python version, if you want to explicitly set it (Optional)")
mark_as_advanced(Python_REQUIRED_VERSION)
mark_as_advanced(Python_ROOT_DIR)
if(Python_REQUIRED_VERSION)
  find_package(Python ${Python_REQUIRED_VERSION} EXACT COMPONENTS Interpreter Development REQUIRED)
else()
  find_package(Python 3.12 COMPONENTS Interpreter Development REQUIRED)
endif()


include_directories("${Python_INCLUDE_DIRS}")

get_filename_component(RESOLVED_PYTHON_LIBRARY "${Python_LIBRARIES}" REALPATH)
message("Python_LIBRARIES=${Python_LIBRARIES}")
message("RESOLVED_PYTHON_LIBRARY=${RESOLVED_PYTHON_LIBRARY}")

add_executable(test main.cpp)
target_link_libraries(test PUBLIC ${Python_LIBRARIES})

install(TARGETS test
  RUNTIME DESTINATION ./
  LIBRARY DESTINATION ./
  ARCHIVE DESTINATION .
)

install(
  CODE "execute_process(
    COMMAND ${CMAKE_COMMAND}
    -DRESOLVED_PYTHON_LIB=${RESOLVED_PYTHON_LIBRARY}
    -DEXECUTABLE_PATH=\${CMAKE_INSTALL_PREFIX}/test${CMAKE_EXECUTABLE_SUFFIX}
    -P ${PROJECT_SOURCE_DIR}/cmake/PythonGetLibAndLinkUp.cmake
  )")

if(APPLE)
  install(
    CODE "execute_process(
      COMMAND ${CMAKE_COMMAND}
      -DRESOLVED_PYTHON_LIB=${RESOLVED_PYTHON_LIBRARY}
      -DEPLUS_DYNAMIC_LIB_NAME=libenergyplusapi.${CMAKE_VERSION_MAJOR}.${CMAKE_VERSION_MINOR}.${CMAKE_VERSION_PATCH}.dylib
      -DEXECUTABLE_PATH=\${CMAKE_INSTALL_PREFIX}/energyplus${CMAKE_EXECUTABLE_SUFFIX}
      -P ${PROJECT_SOURCE_DIR}/cmake/PythonFixUpOnMac.cmake
    )")
endif()

set(CPACK_GENERATOR "TGZ")
include(CPack)
