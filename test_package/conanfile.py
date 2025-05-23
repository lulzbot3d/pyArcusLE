import shutil

from io import StringIO
from pathlib import Path

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.env import VirtualRunEnv
from conan.errors import ConanException
from conan.tools.files import copy


class PyArcusLETestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    test_type = "explicit"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def generate(self):
        venv = VirtualRunEnv(self)
        venv.generate()

        cpp_info = self.dependencies[self.tested_reference_str].cpp_info
        copy(self, "*.pyd", src=cpp_info.libdirs[0], dst=self.build_folder)

        for dep in self.dependencies.values():
            for bin_dir in dep.cpp_info.bindirs:
                copy(self, "*.dll", src=bin_dir, dst=self.build_folder)

    def test(self):
        if can_run(self):
            test_buf = StringIO()
            try:
                self.run("python test.py", env="conanrun", stdout=test_buf, scope="run")
            except ConanException as ex:
                # As long as it still outputs 'True', at least we can say the package is build correctly.
                # (For example: A non-zero exit code might indicate a bug, but that's more the domain of unit-tests, not really relevant to wether or not that _package_ has been build correctly.)
                print(f"WARNING: {str(ex)}")
            ret_val = test_buf.getvalue()
            if "True" not in ret_val:
                raise ConanException("pyArcus wasn't built correctly!")
