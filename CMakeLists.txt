cmake_minimum_required(VERSION 3.26)
project(ProjectName VERSION 1.0.0 LANGUAGES C CXX)

# 这会影响整个目录树，第三方/子项目有时不希望被你强制成 C++23
# 所以 target 级别如不需要 c++ 23 则需要单独覆盖配置
# target_compile_features(vendor PUBLIC cxx_std_17)
# # PUBLIC 则表示link 了 vendor 的 其它target 至少也要支持 c++ 17  
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# $<CONFIG>, generator expression, 构建系统的配置, 如 Debug, Release, Distribution 等
# ${CMAKE_SYSTEM_NAME}, 目标操作系统, 生成的程序想要运行的操作系统, 不同于 ${hostSystemName}
# ${CMAKE_SYSTEM_PROCESSOR}
# # Windows/MSVC: AMD64
# # Linux/clang: x86_64
# # macOS M: arm64
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/$<CONFIG>-${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}/") # 可执行程序
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/bin/$<CONFIG>-${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}/") # shared lib
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_SOURCE_DIR}/lib/$<CONFIG>-${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}/") # static lib + win 动态库配套的 import lib

option(ANT_WARNINGS "Enable common compiler warnings" ON)
option(ANT_WERROR "Treat warnings as errors" OFF)
set(ANT_SANITIZE "OFF" CACHE STRING "Sanitizers: OFF or comma list (address,undefined,thread,leak)")
option(ANT_LTO "Enable Link Time Optimization" OFF)
option(ANT_DIST "Enable distribution mode" OFF)

function(ant_apply_options target_name)
  if (ANT_WARNINGS)
    if (MSVC)
      target_compile_options(${target_name} PRIVATE /W4)
    else()
      target_compile_options(${target_name} PRIVATE -Wall -Wextra -Wpedantic)
    endif()
  endif()

  if (ANT_WERROR)
    if (MSVC)
      target_compile_options(${target_name} PRIVATE /WX)
    else()
      target_compile_options(${target_name} PRIVATE -Werror)
    endif()
  endif()

  # Sanitizers（只对 clang/gcc）
  if (NOT ANT_SANITIZE STREQUAL "OFF")
    if (MSVC)
      message(WARNING "Sanitizers via ANT_SANITIZE are not enabled for MSVC in this template.")
    else()
      # 允许 ANT_SANITIZE="address,undefined"
      # list: 本质是 ; 分隔的字符串
      string(REPLACE "," ";" _san_list "${ANT_SANITIZE}")
      string(JOIN "," _san_csv ${_san_list})

      target_compile_options(${target_name} PRIVATE -fsanitize=${_san_csv} -fno-omit-frame-pointer)
      target_link_options(${target_name} PRIVATE -fsanitize=${_san_csv})
    endif()
  endif()

  # LTO（跨平台方式：CMake 原生）
  if (ANT_LTO)
    include(CheckIPOSupported)
    check_ipo_supported(RESULT _ipo_ok OUTPUT _ipo_msg)
    if (_ipo_ok)
      set_property(TARGET ${target_name} PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    else()
      message(WARNING "IPO/LTO not supported: ${_ipo_msg}")
    endif()
  endif()
  
   # 是否启用日志打印
  if(ANT_LOGGING)
    target_compile_definitions(${target_name} PRIVATE ANT_ENABLE_LOG=1)
  else()
    target_compile_definitions(${target_name} PRIVATE ANT_ENABLE_LOG=0)
  endif()
endfunction()

# ========================
#   Dependencies
# ========================

find_package(spdlog CONFIG REQUIRED)

# 对于全局要用的库, 创建一个全局依赖接口集合, 子模块直接 link ProjectDeps 即可
# 其它 依赖库可以在 spdlog::spdlog 之后补充
add_library(ProjectDeps INTERFACE) 
target_link_libraries(ProjectDeps INTERFACE spdlog::spdlog)

add_subdirectory(src/project)
add_subdirectory(src/sandbox)