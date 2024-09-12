# pyArcusLE

[![Conan Badge]][Conan]

[![Size Badge]][Size]
[![License Badge]][License]

This library contains Python bindings, for libArcusLE, for creating a socket in a thread and using this socket to send and receive messages
based on the Protocol Buffers library. It is designed to facilitate the communication between CuraLE and its backend and similar code.

## License

pyArcusLE is released under terms of the LGPLv3 License. Terms of the license can be found in the LICENSE file or [on the GNU website.](https://www.gnu.org/licenses/lgpl-3.0.html#license-text)

> In general it boils down to:  
> **You need to share the source of any pyArcusLE modifications if you make an application with pyArcusLE.**

## System Requirements

### Windows

- Python 3.6 or higher
- Ninja 1.10 or higher
- VS2022 or higher
- CMake 3.23 or higher
- nmake
- sip 6.5.0 or higher
- Conan 1.56.0

### MacOS

- Python 3.6 or higher
- Ninja 1.10 or higher
- apply clang 11 or higher
- CMake 3.23 or higher
- make
- sip 6.5.0 or higher
- Conan 1.56.0

### Linux

- Python 3.6 or higher
- Ninja 1.10 or higher
- gcc 12 or higher
- CMake 3.23 or higher
- make
- sip 6.5.0 or higher
- Conan 1.56.0

## How To Build

> **Note:**  
> We are currently in the process of switch our builds and pipelines to an approach which uses [Conan](https://conan.io/)
> and pip to manage our dependencies, which are stored on our JFrog Artifactory server and in the pypi.org.
> At the moment not everything is fully ported yet, so bare with us.

If you have never used [Conan](https://conan.io/) read their [documentation](https://docs.conan.io/en/latest/index.html)
which is quite extensive and well maintained. Conan is a Python program and can be installed using pip

### 1. Configure Conan

```bash
pip install conan==1.56
conan config install https://github.com/lulzbot3d/conan-config-le.git
conan profile new default --detect --force
```

Community developers would have to remove the Conan cura-le repository because it requires credentials.

```bash
conan remote remove cura-le
```

### 2. Clone pyArcusLE

```bash
git clone https://github.com/lulzbot3d/pyArcusLE.git
cd pyArcusLE
```

### 3. Install & Build pyArcusLE (Release OR Debug)

#### Release

```bash
conan install . --build=missing --update
# optional for a specific version: conan install . pyarcusle/<version>@<user>/<channel> --build=missing --update
conan build .
# or
sip-install
```

#### Debug

```bash
conan install . --build=missing --update build_type=Debug
conan build .
# or
sip-install
```

## Creating a new pyArcusLE Conan package

To create a new pyArcusLE Conan package such that it can be used in CuraLE and UraniumLE, run the following command:

```shell
conan create . pyarcusle/<version>@<username>/<channel> --build=missing --update
```

This package will be stored in the local Conan cache (`~/.conan/data` or `C:\Users\username\.conan\data` ) and can be used in downstream
projects, such as CuraLE and UraniumLE by adding it as a requirement in the `conanfile.py` or in `conandata.yml`.

Note: Make sure that the used `<version>` is present in the conandata.yml in the pyArcusLE root

You can also specify the override at the commandline, to use the newly created package, when you execute the `conan install`
command in the root of the consuming project, with:

```shell
conan install . -build=missing --update --require-override=pyarcusle/<version>@<username>/<channel>
```

## Developing pyArcusLE In Editable Mode

You can use your local development repository downsteam by adding it as an editable mode package.
This means you can test this in a consuming project without creating a new package for this project every time.

```bash
    conan editable add . pyarcusle/<version>@<username>/<channel>
```

Then in your downsteam projects (CuraLE) root directory override the package with your editable mode package.

```shell
conan install . -build=missing --update --require-override=pyarcusle/<version>@<username>/<channel>
```

## pyArcusLE python module

This repository contains a Python module named pyArcusLE. To build it, [sip](https://pypi.org/project/sip/) 6.5.1 needs to be used to generate the C/C++ source code. UltiMaker created a build tool for this called [sipbuildtool, the repo for which we have also forked](https://github.com/lulzbot3d/conan-lulzbot-index/recipes/sipbuildtool/conanfile.py), which is automatically installed when you run the `conan install` command. This will set up a temporary virtual Python environment, install sip and generate the C/C++ source code. The virtual Python environment is then removed. Downside of this method is that Conan should be installed with the system Python, not the virtual Python environment.

### Usage

```python
import pyArcus
socket = pyArcus.Socket()
```

## Using the Socket

The socket assumes a very simple and strict wire protocol: one 32-bit integer with a header, one 32-bit integer with the message size, one 32-bit integer with a type id then a byte array containing the message as serialized by Protobuf. The receiving side checks for these fields and will deserialize the message, after which it can be processed by the application.

To send or receive messages, the message first needs to be registered on both sides with a call to `registerMessageType()`. You can also register all messages from a Protobuf .proto file with a call to `registerAllMessageTypes()`. For the Python bindings, this is the only supported way of registering since there are no Python classses for individual message types.

The Python bindings expose the same API as the Public C++ API, except for the missing `registerMessageType()` and the individual messages. The Python bindings wrap the messages in a class that exposes the message's properties as Python properties, and can thus be set the same way you would set any other Python property.

The exception is repeated fields. Currently, only repeated messages are supported, which can be created through the `addRepeatedMessage()` method. `repeatedMessageCount()` will return the number of repeated messages on an object and `getRepeatedMessage()` will get a certain instance of a repeated message. See python/PythonMessage.h for more details.

## Origin of the Name

The name Arcus is from the Roman god Arcus. This god is the roman equivalent of
the goddess Iris, who is the personification of the rainbow and the messenger
of the gods.

<!----------------------------------------------------------------------->

[Conan Badge]: https://img.shields.io/github/actions/workflow/status/lulzbot3d/pyArcusLE/conan-package.yml?style=for-the-badge&color=C1D82F&labelColor=788814&logoColor=white&logo=Conan&label=Conan%20Package
[Size Badge]: https://img.shields.io/github/repo-size/lulzbot3d/pyArcusLE?style=for-the-badge&color=CCCCCC&labelColor=666666&logoColor=white&logo=GoogleAnalytics
[License Badge]: https://img.shields.io/github/license/lulzbot3d/pyArcusLE?style=for-the-badge&color=A32D2A&labelColor=511615&logoColor=white&logo=GNU

[Conan]: https://github.com/lulzbot3d/pyArcusLE/actions/workflows/conan-package.yml
[Size]: https://github.com/lulzbot3d/pyArcusLE
[License]: LICENSE
