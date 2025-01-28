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
pip3 install --user .
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

```sh
detloclcheck create_checkerboard_image -outfile foo.png -size 23
detloclcheck find_checkerboard -f foo.png
detloclcheck visualize foo.json -i foo.png
```

```py
import cv2
import json

import matplotlib.pyplot
import numpy

image_name = 'foo.png'
data_name = 'foo.json'
gray_image = cv2.imread(image_name, cv2.COLOR_BGR2GRAY)
with open(data_name) as fd:
    data = json.load(fd)
coordinate_system = numpy.array(data['coordinate_system'])
zeropoint = numpy.array(data['zeropoint'])
matplotlib.pyplot.imshow(gray_image, cmap="Greys")
matplotlib.pyplot.plot(
    coordinate_system[:, 0, 0], coordinate_system[:, 0, 1],
    'r2', markersize=20)
matplotlib.pyplot.plot(zeropoint[0], zeropoint[1], 'b1', markersize=20)
for i in range(coordinate_system.shape[0]):
    matplotlib.pyplot.text(
        coordinate_system[i, 0, 0], coordinate_system[i, 0, 1],
        f'({int(coordinate_system[i, 1, 0])},'
        f'{int(coordinate_system[i, 1, 1])})',
        color='g', fontsize='small', rotation=45)
matplotlib.pyplot.show()
```

## copyright + license

Author: Daniel Mohr.

Date: 2025-01-28 (last change).

License: LGPL-3.0-or-later

Copyright (C) 2024, 2025 Daniel Mohr
