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
    PRIVATE 
        SPDLOG)

target_compile_definitions(Project
    # 编译时添加的宏
    # PRIVATE 表示不传递
    PRIVATE
        PROJECT_BUILD
) 

# 如果是静态库可以像下面这样
# target_compile_definitions(Project 
#     PUBLIC 
#         PROJECT_STATIC
# )