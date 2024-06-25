# README: DetLocLCheck -- Detection, Localization, Checkerboard, L marker

## intro

`DetLocLCheck` is a software tool for Detection and Localization of a
Checkerboard calibration target containing L shape marker using
template matching.

## install

Before you install `DetLocLCheck` you have to provide the dependencies.

We need at least the following debian package:

* `python3-hatchling`
* `python3-numpy`
* `python3-opencv`
* `python3-pip`

`numpy` is defined as dependency in `pyproject.toml`. But we strongly
recommend to use the package from the package management system of your
operating system.

`opencv-python` is not defined as dependency in `pyproject.toml`. The reason
is that `pip` ignores the package from the package management system from the
operating system. As before we strongly recommended to use the package from the
package management system of your operating system.

If you really want not to use it from your package management system you can
install it like `pip3 install opencv-python`. But this is not recommended!

The recommended way to install `DetLocLCheck` is:

```sh
pip3 install --break-system-packages --user .
```

## copyright + license

Author: Daniel Mohr.

Date: 2024-06-25 (last change).

License:

Copyright (C) 2024 Daniel Mohr
