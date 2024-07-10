"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-10
:License: LGPL-3.0-or-later
:Copyright: (C) 2024 Daniel Mohr
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
        m, n, size,
        zeropoint=None, integrate_method=0, transition_value=128, scale=1.0):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-10
    :License: LGPL-3.0-or-later

    Example:

    >>> from detloclcheck.create_checkerboard_image import \
    ...    create_checkerboard_image
    >>> image = create_checkerboard_image(8, 8, 15)
    >>> import cv2
    >>> cv2.imwrite("foo.png", image)
    """
    image_size = (int(numpy.ceil(m*size)),
                  int(numpy.ceil(n*size)))
    if zeropoint is None:
        zeropoint = (image_size[0]/2 - 0.5, image_size[1]/2 - 0.5)
    image = numpy.zeros(
        image_size,
        dtype=numpy.uint8)
    checkerboard_image = CheckerboardImageClass(
        size, zeropoint,
        integrate_method, transition_value)
    for i in range(image_size[0]):
        for j in range(image_size[1]):
            image[i, j] = int(checkerboard_image(i, j))
    return cv2.resize(
        image,
        (int(scale*image.shape[1]), int(scale*image.shape[0])),
        interpolation=cv2.INTER_AREA)
