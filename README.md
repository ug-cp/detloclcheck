# README: DetLocLCheck -- Detection, Localization, Checkerboard, L marker

## intro

`DetLocLCheck` is a software tool for Detection and Localization of a
Checkerboard calibration target containing L shape marker using
template matching.

## install

Before you install `DetLocLCheck` you have to provide the dependencies.

We need at least the following Debian packages:

* `python3-numpy` ([numpy.org](https://numpy.org/))
* `python3-opencv` ([opencv.org](https://opencv.org))
* `python3-pip` ([pip.pypa.io](https://pip.pypa.io/))

On Ubuntu 22.04 do not install (these versions are too old!):

* `python3-hatchling`
* `python3-pathspec`

`numpy` is defined as dependency in `pyproject.toml`. But we strongly
recommend to use the package from the package management system of your
operating system.

`opencv-python` is not defined as dependency in `pyproject.toml`. The reason
is that `pip` ignores the package from the package management system from the
operating system. As before we strongly recommend to use the package from the
package management system of your operating system.

If you really want not to use it from your package management system you can
install it like `pip3 install opencv-python`. But this is not recommended!

The recommended way to install `DetLocLCheck` is:

```sh
pip3 install --break-system-packages --user .
```

On Ubuntu 22.04 the new flag `--break-system-packages` is not available and
you should do:

```sh
pip3 install --break-system-packages --user .
```

For development you could install an editable version, e. g.:

```sh
pip3 install --break-system-packages -e .
```

But this is only working from Python 3.10 on.

## Example

```sh
detloclcheck find_checkerboard -log_file cam.log -run_parallel \
    -crosssizes 35 55 -min_sharpness 25 50 100 -f *.png
```

## copyright + license

Author: Daniel Mohr.

Date: 2024-08-28 (last change).

License: LGPL-3.0-or-later

Copyright (C) 2024 Daniel Mohr
