#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class LibnameConan(ConanFile):
    name = "zstd"
    version = "1.3.2"
    url = "https://github.com/bincrafters/conan-zstd"
    description = "Zstandard - Fast real-time compression algorithm"
    license = "https://raw.githubusercontent.com/facebook/zstd/dev/LICENSE"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports_sources = ['CMakeLists.txt']
    generators = ['cmake', 'txt']

    def source(self):
        source_url = "https://github.com/facebook/zstd"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["ZSTD_BUILD_PROGRAMS"] = False
        cmake.definitions["ZSTD_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["ZSTD_BUILD_SHARED"] = self.options.shared
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = self.package_folder

        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
