cmake_minimum_required(VERSION 3.20)
project(fortran_mcve NONE)

include(CMakeAddFortranSubdirectory.cmake)

cmake_add_fortran_subdirectory(
  sub
  PROJECT SubFortran
  NO_EXTERNAL_INSTALL)
