## Table of Contents

- [Description](#description)
- [Installation](#installation)
  - [Binary packages](#binary-packages)
  - [Direct installation from git](#direct-installation-from-git)
- [Build app binaries for target platform](#build-app-binaries-for-target-platform)
  - [Android](#build-for-android)
  - [Android (with Docker)](#build-for-android-docker)
  - [Windows](#build-for-windows)
  - [Linux](#build-for-linux)
- [Support](#support)
- [Links](#links)
- [Licenses](#licenses)

## Description
### Cross-platform app for small arms ballistic calculations based on python3
- Uses [py_ballisticcalc](https://github.com/o-murphy/py_ballisticcalc) library in backend
- Uses [Kivy GUI framework](https://github.com/kivy/kivy) and [KivyMD](https://github.com/kivymd/KivyMD) for the frontend
- Compatible with [ArcherBC2](https://github.com/JAremko/ArcherBC2) **.a7p** file format

## Installation
### Binary packages:
You can download binaries from **[Releases section](https://github.com/o-murphy/eballistica_app/releases)** of this repo
### Direct installation from git:
#### 1. Download specific release
```shell
# latest (nightly) release, newest changes would be here
git clone https://github.com/o-murphy/eballistica_app

# dev release, there would be more stable versions
git clone -b kivymd-dev https://github.com/o-murphy/eballistica_app 

# latest stable version
git clone -b kivymd-main https://github.com/o-murphy/eballistica_app 
```
#### 2. Create and activate new venv
```shell
python3 -m venv venv
. venv/bin/activate
```
#### 3. Install requirements depends on platform
```shell
pip install -r requirements.txt # Windows OS
pip install -r requirements-linux.txt # Linux based OS 
```
#### 4. Run app
```shell
python3 main.py
```

## Build app binaries for target platform
#### Android with [kivy/buildozer](https://github.com/kivy/kivy)
```shell
# install buildozer from PyPi
pip install buildozer
# build in debug mode
buildozer android debug
```
#### Android with [buildozer](https://github.com/kivy/kivy) in Docker
```shell
# bind your source folder to hostcwd directory of the Docker container
# build in debug mode
docker pull omurphyslaw/buildozer:test
docker run -v "path-to-sources:/home/user/hostcwd" -d omurphyslaw/buildozer:test android debug
# or use branch with preinstalled SDK/NDK
docker pull omurphyslaw/buildozer:SDK31-NDKr25b
docker run -v "path-to-sources:/home/user/hostcwd" -d omurphyslaw/buildozer::SDK31-NDKr25b android debug

```


#### Windows
```shell
# install pyinstaller wia pip
pip install pyinstaller
# or
pip install pyinstaller==5.6.2  # (recommended)
# build binaries
pyinstaller pyinstaller.spec
# make installer
ISCC setup_x64.iss
```

#### Linux
```shell
# install pyinstaller wia pip
pip install pyinstaller
# or
pip install pyinstaller==5.12.0  # (recommended)
# build binaries
pyinstaller pyinstaller-linux.spec
```

## Support
[Issues tracker](https://github.com/o-murphy/eballistica_app/issues)

## Links
- [py_ballisticcalc](https://github.com/o-murphy/py_ballisticcalc): LGPL library for small arms ballistic calculations
- [ArcherBC2](https://github.com/JAremko/ArcherBC2): Cross-platform app for managing ballistic profiles in .a7p format
- [a7p_transfer](https://github.com/JAremko/a7p_transfer_example) and [a7p for python](https://github.com/o-murphy/a7p): libraries and examples of .a7p profiles manage
- [Kivy](https://github.com/kivy/kivy): open source, cross-platform Python framework for the development of applications
- [KivyMD](https://github.com/kivymd/KivyMD): Material widgets for Kivy framework
- [Buildozer](https://github.com/kivy/buildozer): generic Python packager
  for Android and iOS.
- [Python for Android](https://github.com/kivy/python-for-android): toolchain
  for building and packaging Python applications for Android.
- [Pyjnius](https://github.com/kivy/pyjnius): dynamic access to the Java/Android
  API from Python.
- [Pyobjus](https://github.com/kivy/pyobjus): dynamic access to the
  Objective-C/iOS API from Python.
- [Kivy iOS](https://github.com/kivy/kivy-ios): toolchain for building and
  packaging Kivy applications for iOS.
- [Garden](https://github.com/kivy-garden): widgets and libraries created and
  maintained by users.

## Licenses

- Kivy is released under the terms of the MIT License. Please refer to the
  LICENSE file.
- The provided fonts Roboto and Roboto Mono are licensed and
  distributed under the terms of the
  [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
  The DejaVuSans (used for the virtual keyboard) license can be viewed
  [here](https://github.com/dejavu-fonts/dejavu-fonts/blob/master/LICENSE).
- The current UI design has been adapted from Moblintouch theme's SVGs
  and is licensed under the terms of the
  [LGPLv2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1).
