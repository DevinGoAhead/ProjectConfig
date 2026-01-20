#pragma once

#include "PlatformDetection.h" // IWYU pragma: keep

#ifdef ANT_PLATFORM_WINDOWS
	#ifndef NOMINMAX
		// See github.com/skypjack/entt/wiki/Frequently-Asked-Questions#warning-c4003-the-min-the-max-and-the-macro
		#define NOMINMAX
	#endif
#endif


#include <iostream> 		// IWYU pragma: keep
#include <memory> 			// IWYU pragma: keep
#include <utility>  		// IWYU pragma: keep
#include <algorithm>		// IWYU pragma: keep
#include <functional>		// IWYU pragma: keep

#include <string>		// IWYU pragma: keep
#include <sstream>		// IWYU pragma: keep
#include <array>		// IWYU pragma: keep
#include <vector>		// IWYU pragma: keep
#include <unordered_map>		// IWYU pragma: keep
#include <unordered_set>		// IWYU pragma: keep

#include <cstdint> 		// IWYU pragma: keep


#ifdef ANT_PLATFORM_WINDOWS
	#include <Windows.h>
#endif
