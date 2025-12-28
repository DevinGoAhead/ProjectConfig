#ifdef PROJECT_STATIC
  #define PROJECT_API
#endif

#ifdef PROJECT_BUILD
    #define PROJECT_API PROJECT_API_EXPORT
#else
    #define PROJECT_API PROJECT_API_IMPORT
#endif



#if defined (_WIN32) || defined (_WIN64)
    #define PROJECT_API_EXPORT __declspec(dllexport)
    #define PROJECT_API_IMPORT __declspec(dllimport)
#elif defined(__GNUC__) || defined(__clang__)
    #define PROJECT_API_EXPORT __attribute__((visibility("default")))
    #define PROJECT_API_IMPORT
#else 
    #define PROJECT_API_EXPORT
    #define PROJECT_API_IMPORT
#endif