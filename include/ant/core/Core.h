#include "ant/core/PlatformDetection.h"


#if defined ANT_PLATFORM_WINDOWS
    #define ANT_API_EXPORT __declspec(dllexport)
    #define ANT_API_IMPORT __declspec(dllimport)
#elif defined(__GNUC__) || defined(__clang__) || defined(ANT_PLATFORM_LINUX)
    #define ANT_API_EXPORT __attribute__((visibility("default")))
    #define ANT_API_IMPORT
#else 
    #define ANT_API_EXPORT
    #define ANT_API_IMPORT
#endif


#ifdef ANT_STATIC
  #define ANT_API
#endif

#ifdef ANT_BUILD
    #define ANT_API ANT_API_EXPORT
#else
    #define ANT_API ANT_API_IMPORT
#endif

#define BIT(x) 1U << x