#pragma once

#ifdef _WIN32
	/* Windows x64/x86 */
	#ifdef _WIN64
		/* Windows x64  */
		#define PROJ_PLATFORM_WINDOWS
	#else
		/* Windows x86 */
		#error "x86 Builds are not supported!"
	#endif
#elif defined(__APPLE__) || defined(__MACH__)
	#include <TargetConditionals.h>
	/* TARGET_OS_MAC exists on all the platforms
	 * so we must check all of them (in this order)
	 * to ensure that we're running on MAC
	 * and not some other Apple platform */
	#if TARGET_IPHONE_SIMULATOR == 1
		#error "IOS simulator is not supported!"
	#elif TARGET_OS_IPHONE == 1
		#define PROJ_PLATFORM_IOS
		#error "IOS is not supported!"
	#elif TARGET_OS_MAC == 1
		#define PROJ_PLATFORM_MACOS
		#error "MacOS is not supported!"
	#else
		#error "Unknown Apple platform!"
	#endif
/* We also have to check __ANDROID__ before __linux__
 * since android is based on the linux kernel
 * it has __linux__ defined */
#elif defined(__ANDROID__)
	#define PROJ_PLATFORM_ANDROID
	#error "Android is not supported!"
#elif defined(__linux__)
	#define PROJ_PLATFORM_LINUX
#else
	/* Unknown compiler/platform */
	#error "Unknown platform!"
#endif // End of platform detection



#if defined PROJ_PLATFORM_WINDOWS
    #define PROJECT_API_EXPORT __declspec(dllexport)
    #define PROJECT_API_IMPORT __declspec(dllimport)
#elif defined(__GNUC__) || defined(__clang__)
    #define PROJECT_API_EXPORT __attribute__((visibility("default")))
    #define PROJECT_API_IMPORT
#else 
    #define PROJECT_API_EXPORT
    #define PROJECT_API_IMPORT
#endif


#ifdef PROJECT_STATIC
  #define PROJECT_API
#endif

#ifdef PROJECT_BUILD
    #define PROJECT_API PROJECT_API_EXPORT
#else
    #define PROJECT_API PROJECT_API_IMPORT
#endif