"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-09
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


def create_checkerboard_image(args):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-09
    :License: LGPL-3.0-or-later
    """
    image_size = (int(numpy.ceil(args.m[0]*args.size[0])),
                  int(numpy.ceil(args.n[0]*args.size[0])))
    if args.zeropoint is None:
        args.zeropoint = (image_size[0]/2, image_size[1]/2)
    image = numpy.zeros(
        image_size,
        dtype=numpy.uint8)
    checkerboard_image = CheckerboardImageClass(
        args.size[0], args.zeropoint, args.integrate_method[0])
    for i in range(image_size[0]):
        for j in range(image_size[1]):
            image[i, j] = int(checkerboard_image(i, j))
    return cv2.resize(
        image,
        (int(args.scale[0]*image.shape[1]), int(args.scale[0]*image.shape[0])),
        interpolation=cv2.INTER_AREA)
