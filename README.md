# CMakeLists.txt
```cmake
# 当前 target 为 A 
# target B link 到 A
PUBLIC # B 在编译“自己的 cpp”时, 会传递给 B
PRIVATE # 仅 A 生效
INTERFACE # 当A 为header_only 时用, 针对 B 生效, 对 A 无效
```
# CMakePresets.json
```json
// ${hostSystemName} - CMake 工作的那台机器的操作系统名, 如 Windows, Linux
// ${presetName} - "name": "linux-debug",
// 最终效果:
// build/Linux/linux-debug
// build/Linux/linux-release
"binaryDir": "${sourceDir}/build/${hostSystemName}/${presetName}"

// 通常只在 win 下需要, 目的是指定 find_packag 的工作目录
// 之后把这个配置删掉了, 我直接放到了vender 下
"CMAKE_PREFIX_PATH": "D:/.local"
```
## 警告配置
### 警告选项解释
#### MSVC
```cmake
/W0 # 几乎无警告
/W3 # MSVC 的传统“默认推荐等级”

# 报警最多, 如
# # 有风险的隐式转换
# # signed/unsigned 混用
# # 潜在未初始化
# # switch 不完整
# # 一些历史遗留设计问题
/W4 

/WX # 所有 warning 当作 error
```
#### GCC / Clang
```cmake
-Wall # 打开大多数有价值的警告, 但不是全部
-Wextra # 更多警告, 如 未使用参数, 边界 case 等
-Wpedantic # 语言标准洁癖模式, 如非标准扩展会警告（GNU 扩展、MS 扩展）
# 上述三者合在一起 ≈ /W4

-Werror # 等价与 /W4
```
```
这里不再贴 CMakePresets.json 的源码
```
### CMakeLists.txt 中与 CMakePreset.json 中对应的配置
```cmake
# option(<variable> "<help_text>" [value])
# 如果 cache 中没有这个变量, 则创建一个并设置默认值, 反之则什么也不做
# option 会创建一个 boolean 变量, value 默认值为 OFF
# # CMakePrests.json 中
# # "cacheVariables": { "ANT_WARNINGS": "ON"} 相当于重新给变量赋值
option(ANT_WARNINGS "Enable common compiler warnings" ON)
option(ANT_WERROR "Treat warnings as errors" OFF)

# 创建一个 CACHE STRING 类型的变量. 默认值 OFF
# 变量可有四种选项, 可被以下操作覆盖
# # cmake -DANT_SANITIZE=address, ---指令
# # CMakePresets.json, ---Preset
# # GUI（ccmake / cmake-gui）, ---GUI
# 四种选项的含义, 见 OneNote 相关
set(ANT_SANITIZE "OFF" CACHE STRING "Sanitizers: OFF or comma list (address,undefined,thread,leak)")
option(ANT_LTO "Enable Link Time Optimization" OFF)
option(ANT_DIST "Enable distribution mode" OFF)
```

```cmake
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
      # 规范化, 将所有 , 替换为 ;
      # 以 ; 间隔的字符串称为 cmake list
      # JOIN 结构化操作, 将 ; 替换回 ,
      string(REPLACE "," ";" _san_list "${ANT_SANITIZE}")
      string(JOIN "," _san_csv ${_san_list})
      # JOIN 结构化操作, 将 ; 替换回 ,
      target_compile_options(${target_name} PRIVATE -fsanitize=${_san_csv} -fno-omit-frame-pointer)
      target_link_options(${target_name} PRIVATE -fsanitize=${_san_csv})
    endif()
  endif()

  # LTO（跨平台方式：CMake 原生）
  # link 变慢，但可执行性能/体积可能更好
  if (ANT_LTO)
    include(CheckIPOSupported)
    check_ipo_supported(RESULT _ipo_ok OUTPUT _ipo_msg)
    if (_ipo_ok)
      set_property(TARGET ${target_name} PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    else()
      message(WARNING "IPO/LTO not supported: ${_ipo_msg}")
    endif()
  endif()
endfunction()

```
## 编译器/构建器配置
```json
// 这里主要是为了控制 CMake 的GUI 中是否显示该配置, 等价于
// if(${hostSystemName} == "Windows) 才显示该配置
"condition": {
    "type": "equals",
    "lhs": "${hostSystemName}",
    "rhs": "Windows"
}

// 如果用的是 Visual Studio 生成器，CMake 可以直接传参数告诉 VS 怎么做

// 但我这里用的是 Ninja
// Ninja 无法知道什么是 x64 环境
// 设置成 external 后，VS Code（CMake Tools 插件）会在后台运行 vcvarsall.bat x64，把环境变量配好，然后再启动 CMake
"architecture": {
    "value": "x64",
    "strategy": "external"
}

// value: "host=x64"：
// 这指的是编译器程序 (cl.exe) 本身是 32位还是 64位
"toolset": {
    "value": "host=x64",
    "strategy": "external"
}
```
# .clangd
```yaml
# 这是 compile_command.json 所在的目录, 如果出现找不到头文件的情况, 可能需要调整这里
CompilationDatabase: ./
```

# compile_commands.json
*将目标 compile_commands.json "拷贝" 一份*
```bash
# linux 
# linux-clang-debug -- preset name
python3 SyCC.py --preset linux-clang-debug
```

```powershell
# pwsh
# windows-msvc-debug -- preset name
python SyCC.py --preset windows-msvc-debug
```