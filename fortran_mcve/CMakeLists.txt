cmake_minimum_required(VERSION 3.20)
project(fortran_mcve C CXX)

list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake_modules")

include(CMakeAddFortranSubdirectory)

cmake_add_fortran_subdirectory(
  sub
  PROJECT SubFortran
  NO_EXTERNAL_INSTALL)
