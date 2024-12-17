#include <iostream>

const int numStandards = 7;
const long stdCode[numStandards] = { 
    199711L, 201103L, 201402L, 201703L, 
    202002L, 202302L, 202612L
};
const char* stdName[numStandards] = { 
    "Pre-C++11", "C++11", "C++14", "C++17", 
    "C++20", "C++23", "C++26" 
};

long getCPPStandard() {
#if defined (_MSVC_LANG)
    return _MSVC_LANG;
#else
    return __cplusplus;
#endif
}

int main() {
    long standard = getCPPStandard();
    for (int i = 0; i < numStandards; ++i) {
        if (standard == stdCode[i]) {
            std::cout << "Using " << stdName[i] << "\n";
            break;
        }
    }
    return 0;
}