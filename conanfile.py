#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class ZstdConan(ConanFile):
    name = "zstd"
    version = "1.3.8"
    url = "https://github.com/bincrafters/conan-zstd"
    homepage = "https://github.com/facebook/zstd"
    description = "Zstandard - Fast real-time compression algorithm"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "zstd", "compression", "algorithm", "decoder")
    license = "BSD-3-Clause"
    exports = ["LICENSE.md"]
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"

    def source(self):
        sha256 = "90d902a1282cc4e197a8023b6d6e8d331c1fd1dfe60f7f8e4ee9da40da886dc3"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ZSTD_BUILD_PROGRAMS"] = False
        cmake.definitions["ZSTD_BUILD_STATIC"] = not self.options.shared
        cmake.definitions["ZSTD_BUILD_SHARED"] = self.options.shared
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
