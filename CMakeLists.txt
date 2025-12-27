cmake_minimum_required(VERSION 3.26)
project(AutoPipe VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_definitions(-D_DEBUG)
endif()


# ========================
#   Dependencies
# ========================

find_package(Eigen3 REQUIRED)

find_package(VTK REQUIRED COMPONENTS
    CommonCore
    CommonDataModel
    FiltersCore
    FiltersGeneral
    RenderingCore
    RenderingOpenGL2
    InteractionStyle
)

find_package(OpenCASCADE REQUIRED COMPONENTS
    FoundationClasses ModelingData ModelingAlgorithms 
    Visualization ApplicationFramework DataExchange
)

find_package(PostgreSQL REQUIRED)

# =========================
#  Create OCCT interface target
# =========================

add_library(OCCT INTERFACE)

target_include_directories(OCCT INTERFACE
    ${OpenCASCADE_INCLUDE_DIR}
)

target_link_libraries(OCCT INTERFACE
    TKernel
    TKMath
    TKG2d
    TKG3d
    TKGeomBase
    TKBRep
    TKGeomAlgo
    TKTopAlgo
    TKOffset
    TKMesh
    TKBool
    TKFillet
    TKShHealing
    TKPrim
    TKHLR
    TKService

    # Mesh / Visualization
    TKMeshVS
    TKV3d
    TKOpenGl

    # Serialization / Storage
    TKCDF
    TKStd
    TKStdL
    TKXml
    TKXmlL
    TKBin
    TKBinL

    # CAF / XCAF
    TKCAF
    TKLCAF
    TKXCAF
    TKVCAF
    TKDCAF
    TKXmlXCAF
    TKBinXCAF

    # DataExchange (supported on Ubuntu 7.6.3)
    TKSTEP
    TKSTEPBase
    TKSTEPAttr
    TKSTEP209
    TKIGES
    TKSTL
    TKVRML
)

# ========================
#   Subdirectories
# ========================

add_subdirectory(src/modeling)
add_subdirectory(src/vtksets)
add_subdirectory(src/core)
add_subdirectory(src/data)
add_subdirectory(src/apps)
