# pyArcus

<p align="center">
    <a href="https://github.com/Ultimaker/pyArcus/actions/workflows/conan-package.yml" alt="Conan Package">
        <img src="https://github.com/Ultimaker/pyArcus/actions/workflows/conan-package.yml/badge.svg" /></a>
    <a href="https://github.com/Ultimaker/pyArcus/issues" alt="Open Issues">
        <img src="https://img.shields.io/github/issues/ultimaker/pyArcus" /></a>
    <a href="https://github.com/Ultimaker/pyArcus/issues?q=is%3Aissue+is%3Aclosed" alt="Closed Issues">
        <img src="https://img.shields.io/github/issues-closed/ultimaker/pyArcus?color=g" /></a>
    <a href="https://github.com/Ultimaker/pyArcus/pulls" alt="Pull Requests">
        <img src="https://img.shields.io/github/issues-pr/ultimaker/pyArcus" /></a>
    <a href="https://github.com/Ultimaker/pyArcus/graphs/contributors" alt="Contributors">
        <img src="https://img.shields.io/github/contributors/ultimaker/pyArcus" /></a>
    <a href="https://github.com/Ultimaker/pyArcus" alt="Repo Size">
        <img src="https://img.shields.io/github/repo-size/ultimaker/pyArcus?style=flat" /></a>
    <a href="https://github.com/Ultimaker/pyArcus/blob/master/LICENSE" alt="License">
        <img src="https://img.shields.io/github/license/ultimaker/pyArcus?style=flat" /></a>
</p>

This library contains Python bindings, for libArcus, for creating a socket in a thread and using this socket to send and receive messages
based on the Protocol Buffers library. It is designed to facilitate the communication between Cura and its backend and similar code.

## License

![License](https://img.shields.io/github/license/ultimaker/pyArcus?style=flat)  
pyArcus is released under terms of the LGPLv3 License. Terms of the license can be found in the LICENSE file. Or at
http://www.gnu.org/licenses/lgpl.html

> But in general it boils down to:  
> **You need to share the source of any pyArcus modifications if you make an application with pyArcus.**

## System Requirements

### Windows
- Python 3.6 or higher
- Ninja 1.10 or higher
- VS2022 or higher
- CMake 3.23 or higher
- nmake
- sip 6.5.0 or higher

### MacOs
- Python 3.6 or higher
- Ninja 1.10 or higher
- apply clang 11 or higher
- CMake 3.23 or higher
- make
- sip 6.5.0 or higher

### Linux
- Python 3.6 or higher
- Ninja 1.10 or higher
- gcc 12 or higher
- CMake 3.23 or higher
- make
- sip 6.5.0 or higher


## How To Build

> **Note:**  
> We are currently in the process of switch our builds and pipelines to an approach which uses [Conan](https://conan.io/)
> and pip to manage our dependencies, which are stored on our JFrog Artifactory server and in the pypi.org.
> At the moment not everything is fully ported yet, so bare with us.

If you want to develop Cura with pyArcus see the Cura Wiki: [Running Cura from source](https://github.com/Ultimaker/Cura/wiki/Running-Cura-from-Source)

If you have never used [Conan](https://conan.io/) read their [documentation](https://docs.conan.io/en/latest/index.html)
which is quite extensive and well maintained. Conan is a Python program and can be installed using pip

### 1. Configure Conan

```bash
pip install conan --upgrade
conan config install https://github.com/ultimaker/conan-config.git
conan profile new default --detect --force
```

Community developers would have to remove the Conan cura repository because it requires credentials. 

Ultimaker developers need to request an account for our JFrog Artifactory server at IT
```bash
conan remote remove cura
```

### 2. Clone pyArcus
```bash
git clone https://github.com/Ultimaker/pyArcus.git
cd pyArcus
```

### 3. Install & Build pyArcus (Release OR Debug)

#### Release
```bash
conan install . --build=missing --update
# optional for a specific version: conan install . pyarcus/<version>@<user>/<channel> --build=missing --update
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

## Creating a new pyArcus Conan package

To create a new pyArcus Conan package such that it can be used in Cura and Uranium, run the following command:

```shell
conan create . pyarcus/<version>@<username>/<channel> --build=missing --update
```

This package will be stored in the local Conan cache (`~/.conan/data` or `C:\Users\username\.conan\data` ) and can be used in downstream
projects, such as Cura and Uranium by adding it as a requirement in the `conanfile.py` or in `conandata.yml`.

Note: Make sure that the used `<version>` is present in the conandata.yml in the pyArcus root

You can also specify the override at the commandline, to use the newly created package, when you execute the `conan install`
command in the root of the consuming project, with:


```shell
conan install . -build=missing --update --require-override=pyarcus/<version>@<username>/<channel>
```

## Developing pyArcus In Editable Mode

You can use your local development repository downsteam by adding it as an editable mode package.
This means you can test this in a consuming project without creating a new package for this project every time.

```bash
    conan editable add . pyArcus/<version>@<username>/<channel>
```

Then in your downsteam projects (Cura) root directory override the package with your editable mode package.  

```shell
conan install . -build=missing --update --require-override=pyarcus/<version>@<username>/<channel>
```

## pyArcus python module

This repository contains a Python module named pyArcus. To build it [sip](https://pypi.org/project/sip/) 6.5.1
needs to be used to generate the C/C++ source code. We created a build tool for this called [sipbuildtool](https://github.com/Ultimaker/conan-ultimaker-index/recipes/sipbuildtool/conanfile.py)
which is automatically installed when you run the `conan install` command. This will set up a temporary virtual Python environment, install
sip and generated the C/C++ source code. The virtual Python environment is then removed. Downside of this method is that Conan should be
installed with the system Python, not the virtual Python environment.

#### usage

```python
import pyArcus
socket = pyArcus.Socket()
```

## Using the Socket


The socket assumes a very simple and strict wire protocol: one 32-bit integer with
a header, one 32-bit integer with the message size, one 32-bit integer with a type id
then a byte array containing the message as serialized by Protobuf. The receiving side
checks for these fields and will deserialize the message, after which it can be processed 
by the application.

To send or receive messages, the message first needs to be registered on both sides with 
a call to `registerMessageType()`. You can also register all messages from a Protobuf 
 .proto file with a call to `registerAllMessageTypes()`. For the Python bindings, this 
is the only supported way of registering since there are no Python classses for 
individual message types.

The Python bindings expose the same API as the Public C++ API, except for the missing
`registerMessageType()` and the individual messages. The Python bindings wrap the
messages in a class that exposes the message's properties as Python properties, and
can thus be set the same way you would set any other Python property. 

The exception is repeated fields. Currently, only repeated messages are supported, which
can be created through the `addRepeatedMessage()` method. `repeatedMessageCount()` will
return the number of repeated messages on an object and `getRepeatedMessage()` will get
a certain instance of a repeated message. See python/PythonMessage.h for more details.

## Origin of the Name

The name Arcus is from the Roman god Arcus. This god is the roman equivalent of
the goddess Iris, who is the personification of the rainbow and the messenger
of the gods.

## Java
There is a Java port of pyArcus, which can be found [here](https://github.com/Ocarthon/pyArcus-Java).
