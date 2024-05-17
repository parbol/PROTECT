#----------------------------------------------------------------------------
# Setup the project
cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
project(The-Generator)

#----------------------------------------------------------------------------
# Find Geant4 package, activating all available UI and Vis drivers by default
# You can set WITH_GEANT4_UIVIS to OFF via the command line or ccmake/cmake-gui
# to build a batch mode only executable
#
option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

#----------------------------------------------------------------------------
# Setup Geant4 include directories and compile definitions
# Setup include directory for this project
#
include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)


#----------------------------------------------------------------------------
# Locate sources and headers for this project
# NB: headers are included so they will show up in IDEs
#
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

#----------------------------------------------------------------------------
# Add the executable, and link it to the Geant4 libraries
#
include_directories("$ENV{JSONCPPDIR}/include/")
set(JSONCPP_LIB "$ENV{JSONCPPDIR}/lib/libjsoncpp.a")
find_library(JSONCPP_LIB JSONCPPY $ENV{JSONCPP_LIB_PATH})


##############ADDED FOR JSONCPP#######################

add_executable(Generator Generator.cc ${sources} ${headers})
#target_link_libraries(Generator ${Geant4_LIBRARIES} ${CRY_LIB})
#target_link_libraries(Generator ${Geant4_LIBRARIES} jsoncpp ${CRY_LIB})
target_link_libraries(Generator ${Geant4_LIBRARIES} ${JSONCPP_LIB})
#----------------------------------------------------------------------------
# Copy all scripts to the build directory, i.e. the directory in which we
# build B1. This is so that we can run the executable directly because it
# relies on these scripts being in the current working directory.
#
set(TheWorldFunction_SCRIPTS
  )

foreach(_script ${TheWorldFunction_SCRIPTS})
  configure_file(
    ${PROJECT_SOURCE_DIR}/${_script}
    ${PROJECT_BINARY_DIR}/${_script}
    COPYONLY
    )
endforeach()

#----------------------------------------------------------------------------
# For internal Geant4 use - but has no effect if you build this
# example standalone
#
add_custom_target(The-Generator DEPENDS Generator)

#----------------------------------------------------------------------------
# Install the executable to 'bin' directory under CMAKE_INSTALL_PREFIX
#
install(TARGETS Generator DESTINATION bin)


