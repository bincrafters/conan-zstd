#include <zstd.h>
#include <string>
#include <array>
#include <cstdlib>
#include <iostream>

#define BUFFER_SIZE 1024

int main()
{
    std::array<char, BUFFER_SIZE> uncompressed{"hello"};
    std::array<char, BUFFER_SIZE> compressed;

    const auto compression_result = ZSTD_compress(uncompressed.data(), uncompressed.size(), compressed.data(), compressed.size(), 1);
    if (ZSTD_isError(compression_result)) {
        std::cerr << "error compressing " << ZSTD_getErrorName(compression_result) << std::endl;
        std::abort();
    }
}
