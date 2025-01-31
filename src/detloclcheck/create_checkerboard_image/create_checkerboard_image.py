# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-07-31
:License: LGPL-3.0-or-later
:Copyright: (C) 2024, 2025 Daniel Mohr
"""
# This file is part of DetLocLCheck.
#
# DetLocLCheck free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# DetLocLCheck is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DetLocLCheck. If not, see <https://www.gnu.org/licenses/>.

import cv2
import numpy

from .checkerboard_image_class import CheckerboardImageClass


def create_checkerboard_image(
        width, height, size,
        zeropoint=None, integrate_method=0, transition_value=128, scale=1.0):
    """
    :Author: Daniel Mohr
    :Date: 2025-01-31
    :License: LGPL-3.0-or-later

    Example 1:

    >>> from detloclcheck.create_checkerboard_image import \
    ...    create_checkerboard_image
    >>> _, _, image = create_checkerboard_image(8, 8, 15)
    >>> import cv2
    >>> cv2.imwrite("foo.png", image)

    Example 2:

    >>> from detloclcheck.create_checkerboard_image import \
    ...    create_checkerboard_image
    >>> _, _, image = create_checkerboard_image(8, 8, 15)
    import matplotlib.pyplot
    matplotlib.pyplot.imshow(image)
    matplotlib.pyplot.plot(
    ...     coordinate_system[:,0,0], coordinate_system[:,0,1], 'x')
    matplotlib.pyplot.show()

    Example 3:

    >>> import matplotlib.pyplot
    >>> from detloclcheck.create_checkerboard_image import \
    ...     create_checkerboard_image
    >>> from detloclcheck.detect_localize_checkerboard import \
    ...     detect_localize_checkerboard
    >>> zeropoint, coordinates, image = create_checkerboard_image(8, 8, 15)
    >>> matplotlib.pyplot.imshow(image, cmap="Greys")
    >>> matplotlib.pyplot.plot(coordinates[:,0], coordinates[:,1],
    ...                        'r1', markersize=20)
    >>> matplotlib.pyplot.plot(zeropoint[0], zeropoint[1], 'b2', markersize=20)
    >>> coordinate_system, zeropoint, axis1, axis2 = \
    ...     detect_localize_checkerboard(
    ...         image, crosssizes=(11,),
    ...         angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))
    >>> matplotlib.pyplot.plot(
    ...     coordinate_system[:,0,0], coordinate_system[:,0,1],
    ...     'g3', markersize=20)
    >>> matplotlib.pyplot.show()
    """
    image_size = (int(numpy.ceil(width*size)),
                  int(numpy.ceil(height*size)))
    if zeropoint is None:
        zeropoint = (image_size[0]/2 - 0.5, image_size[1]/2 - 0.5)
    image = numpy.zeros(
        image_size,
        dtype=numpy.uint8)
    checkerboard_image = CheckerboardImageClass(
        size, (zeropoint[1], zeropoint[0]),
        integrate_method, transition_value)
    for i in range(image_size[0]):
        for j in range(image_size[1]):
            image[i, j] = int(checkerboard_image(i, j))
    coordinates = []
    x0 = int(numpy.ceil((0 - zeropoint[0]) / size))
    x1 = int(numpy.floor((image_size[0] - zeropoint[0]) / size))
    y0 = int(numpy.ceil((0 - zeropoint[1]) / size))
    y1 = int(numpy.floor((image_size[1] - zeropoint[1]) / size))
    for x in range(x0, x1):
        for y in range(y0, y1):
            if (x, y) not in [(-2, -2), (-1, -2), (0, -2), (1, -2),
                              (-2, -1), (-1, -1), (0, -1), (1, -1),
                              (-2, 0), (-1, 0),
                              (-2, 1), (-1, 1)]:
                xcoo = zeropoint[0] + x * size
                ycoo = zeropoint[1] + y * size
                if ((3 < xcoo) and (3 + xcoo < image_size[1]) and
                        (3 < ycoo) and (3 + ycoo < image_size[1])):
                    coordinates.append((xcoo, ycoo))
    return zeropoint, numpy.array(coordinates), cv2.resize(
        image,
        (int(scale*image.shape[1]), int(scale*image.shape[0])),
        interpolation=cv2.INTER_AREA)
