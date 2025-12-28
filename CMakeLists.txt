cmake_minimum_required(VERSION 3.26)
project(ProjectName VERSION 1.0.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    add_definitions(-D_DEBUG)
endif()


# ========================
#   Dependencies
# ========================

find_package(spdlog CONFIG REQUIRED)

add_library(SPDLOG INTERFACE) # 对于全局要用的库, 创建一个全局依赖接口集合, 子模块直接 link SPDLOG 即可
target_link_libraries(SPDLOG INTERFACE spdlog::spdlog)

add_subdirectory(src/project)
add_subdirectory(src/sandbox)