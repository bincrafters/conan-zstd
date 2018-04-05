#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ZstdConan(ConanFile):
    name = "zstd"
    version = "1.3.4"
    url = "https://github.com/bincrafters/conan-zstd"
    homepage = "https://facebook.github.io/zstd/"
    description = "Zstandard - Fast real-time compression algorithm"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "BSD"
    exports = ["LICENSE.md"]
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/facebook/zstd"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ZSTD_BUILD_PROGRAMS"] = False
        cmake.definitions["ZSTD_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["ZSTD_BUILD_SHARED"] = self.options.shared
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.configure()
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
