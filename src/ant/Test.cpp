#include "ant/Test.h"
#include <iostream>
#include <print>

namespace AE {
void Print() {
    //std::println("{}", "a");
#ifdef _MSC_VER
    std::cout << "_MSC_VER=" << _MSC_VER << "\n";
#endif
#ifdef _LIBCPP_VERSION
    std::cout << "libc++=" << _LIBCPP_VERSION << "\n";
#endif
#ifdef __GLIBCXX__
    std::cout << "libstdc++\n";
#endif
#ifdef __cpp_lib_print
    std::cout << "__cpp_lib_print=" << __cpp_lib_print << "\n";
#else
    std::cout << "__cpp_lib_print NOT defined\n";
#endif

    std::println("{}", "This is a project template");
}
}  // namespace AE