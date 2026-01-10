#pragma once

#include "project/core/PlatformDetection.h"

#if defined PROJ_PLATFORM_WINDOWS
    #define PROJ_API_EXPORT __declspec(dllexport)
    #define PROJ_API_IMPORT __declspec(dllimport)
#elif defined(__GNUC__) || defined(__clang__)
    #define PROJ_API_EXPORT __attribute__((visibility("default")))
    #define PROJ_API_IMPORT
#else 
    #define PROJ_API_EXPORT
    #define PROJ_API_IMPORT
#endif


#ifdef PROJ_STATIC
  #define PROJ_API
#endif

#ifdef PROJ_BUILD
    #define PROJ_API PROJ_API_EXPORT
#else
    #define PROJ_API PROJ_API_IMPORT
#endif