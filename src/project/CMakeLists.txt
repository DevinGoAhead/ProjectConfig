add_library(Project SHARED Test.cpp)

target_include_directories(Project
    PUBLIC 
        ${PROJECT_SOURCE_DIR}/include # 项目级 include 一定需要被传递, 一定是 PUBLIC
    PRIVATE
        # 如果 glad 头文件仅仅在 Test.cpp 中被 include, 而没有在 Test.h 中被 include, 则不需要被传递, PRIVATE 即可
        # # 反之则 PUBLIC
        # #  INTERFACE 则是针对仅有 .h 而没有 .cpp 的文件
        ${PROJECT_SOURCE_DIR}/vender/glad/include 
) 

# 通常情况下 link 都应该是 PRIVATE
# 因为实现一般都是在 cpp 文件中的, 不会暴露给头文件
target_link_libraries(Project 
    PUBLIC 
        ProjectDeps)

target_compile_definitions(Project
    # 编译时添加的宏
    # PRIVATE 表示不传递
    PRIVATE
        PROJECT_BUILD
    PUBLIC
        # generator expression, "生成构建系统/构建阶段”按条件展开
        # 当配置是 Debug 时, $<CONFIG:Debug> 为 1, 条件为真, ANT_DEBUG 有效
        # 其它类似
        $<$<CONFIG:Debug>:ANT_DEBUG>
        $<$<CONFIG:Release>:ANT_RELEASE>
)

# 就 PROJECT_BUILD 而言, 如果是静态库可以添加其它宏, 如
# target_compile_definitions(Project 
#     PUBLIC 
#         PROJECT_STATIC
# )
# ant_apply_options(Project)

message(STATUS "PROJECT_SOURCE_DIR = ${PROJECT_SOURCE_DIR}")
message(STATUS "CMAKE_SOURCE_DIR   = ${CMAKE_SOURCE_DIR}")
message(STATUS "CMAKE_CURRENT_LIST_DIR = ${CMAKE_CURRENT_LIST_DIR}")