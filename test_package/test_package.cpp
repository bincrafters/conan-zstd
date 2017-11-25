#include <zstd.h>
#include <string>
#include <array>
#include <cstdlib>
#include <iostream>

constexpr auto buffer_size = 1024;

int main()
{
    std::array<char, buffer_size> uncompressed{"hello"};
    std::array<char, buffer_size> compressed;

    const auto compression_result = ZSTD_compress(uncompressed.data(), uncompressed.size(), compressed.data(), compressed.size(), 1);
    if (ZSTD_isError(compression_result)) {
        std::cerr << "error compressing " << ZSTD_getErrorName(compression_result) << std::endl;
        std::abort();
    }
}
