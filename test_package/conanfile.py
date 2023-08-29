import shutil

from io import StringIO
from pathlib import Path

from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.env import VirtualRunEnv
from conan.errors import ConanException


class ArcusTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "VirtualRunEnv"

    def generate(self):
        venv = VirtualRunEnv(self)
        venv.generate()

    def build(self):
        if can_run(self):
            shutil.copy(Path(self.source_folder).joinpath("test.py"), Path(self.build_folder).joinpath("test.py"))
            shutil.copy(Path(self.source_folder).joinpath("test.proto"), Path(self.build_folder).joinpath("test.proto"))

    def test(self):
        if can_run(self):
            test_buf = StringIO()
            self.run(f"python test.py", env = "conanrun", output = test_buf, run_environment=True)
            ret_val = test_buf.getvalue()
            if "True" not in ret_val:
                raise ConanException("pyArcus wasn't build correctly!")
