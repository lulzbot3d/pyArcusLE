import os

from conan.tools.cmake import CMakeToolchain, CMakeDeps, CMake, cmake_layout
from conan.tools import files
from conan import ConanFile
from conans import tools
from conans.errors import ConanException

required_conan_version = ">=1.46.2"


class ArcusConan(ConanFile):
    name = "pyarcus"
    license = "LGPL-3.0"
    author = "Ultimaker B.V."
    url = "https://github.com/Ultimaker/libArcus"
    description = "Communication library between internal components for Ultimaker software"
    topics = ("conan", "python", "binding", "sip", "cura", "protobuf")
    settings = "os", "compiler", "build_type", "arch"
    revision_mode = "scm"
    exports = "LICENSE*"

    python_requires = "umbase/0.1.5@ultimaker/testing", "sipbuildtool/0.1@ultimaker/testing"
    python_requires_extend = "umbase.UMBaseConanfile"

    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True,
    }
    scm = {
        "type": "git",
        "subfolder": ".",
        "url": "auto",
        "revision": "auto"
    }

    def requirements(self):
        for req in self._um_data()["requirements"]:
            self.requires(req)

    def config_options(self):
        if self.options.shared and self.settings.compiler == "Visual Studio":
            del self.options.fPIC

    def configure(self):
        self.options["protobuf"].shared = True
        self.options["cpython"].shared = True

    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, 17)

    def generate(self):
        cmake = CMakeDeps(self)
        cmake.generate()

        tc = CMakeToolchain(self)

        if self.settings.compiler == "Visual Studio":
            tc.blocks["generic_system"].values["generator_platform"] = None
            tc.blocks["generic_system"].values["toolset"] = None

        sip = self.python_requires["sipbuildtool"].module.SipBuildTool(self)
        sip.configure()
        sip.generate("pyArcus")

        tc.variables["Python_EXECUTABLE"] = self.deps_user_info["cpython"].python.replace("\\", "/")
        tc.variables["Python_USE_STATIC_LIBS"] = not self.options["cpython"].shared
        tc.variables["Python_ROOT_DIR"] = self.deps_cpp_info["cpython"].rootpath.replace("\\", "/")
        tc.variables["Python_FIND_FRAMEWORK"] = "NEVER"
        tc.variables["Python_FIND_REGISTRY"] = "NEVER"
        tc.variables["Python_FIND_IMPLEMENTATIONS"] = "CPython"
        tc.variables["Python_FIND_STRATEGY"] = "LOCATION"

        if self.options.shared and self.settings.os == "Windows":
            tc.variables["Python_SITELIB_LOCAL"] = self.cpp.build.bindirs[0].replace("\\", "/")
        else:
            tc.variables["Python_SITELIB_LOCAL"] = self.cpp.build.libdirs[0].replace("\\", "/")

        tc.generate()

    def layout(self):
        self.folders.source = "."
        try:
            build_type = str(self.settings.build_type)
        except ConanException:
            raise ConanException("'build_type' setting not defined, it is necessary for cmake_layout()")
        self.folders.build = f"cmake-build-{build_type.lower()}"
        self.folders.generators = os.path.join(self.folders.build, "conan")
        self.cpp.build.libdirs = ["."]
        self.cpp.build.bindirs = ["."]

        self.cpp.source.includedirs = ["include"]

        self.cpp.build.libdirs = [".", os.path.join("pyArcus", "pyArcus")]

        self.cpp.package.includedirs = ["include"]
        self.cpp.package.libdirs = ["site-packages"]
        self.cpp.package.requires = ["libarcus::libarcus", "protobuf::protobuf", "cpython::cpython"]

        if self.settings.os in ["Linux", "FreeBSD", "Macos"]:
            self.cpp.package.components["pyarcus"].system_libs = ["pthread"]

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        packager = files.AutoPackager(self)
        packager.patterns.build.lib = ["*.so", "*.so.*", "*.a", "*.lib", "*.dylib", "*.pyd", "*.pyi"]
        packager.run()

    def package_info(self):
        if self.in_local_cache:
            self.runenv_info.append_path("PYTHONPATH", self.cpp_info.components["pyarcus"].lib_paths[0])
        else:
            self.runenv_info.append_path("PYTHONPATH", self.build_folder)
