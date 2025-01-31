# SPDX-FileCopyrightText: 2024 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-01
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

import logging

import numpy

from .calculate_sharpness import calculate_sharpness


def filter_blurry_corners(image, coordinates, size, min_sharpness):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-11, 2024-06-13
    :License: LGPL-3.0-or-later

    filter blurry corners in an image of a checkerboard

    :param image: 2 dimensional numpy array describing the image
    :param coordinates: coordinates of the inner corners of the checkerboard
    :param size: int to desribe the window for sharpness calculation
    """
    log = logging.getLogger('detloclcheck.filter_blurry_corners')
    blurry_corners = []
    log.debug('use size = %f for filtering blurry corners', size)
    for i in range(coordinates.shape[0]):
        i0 = int(round(coordinates[i, 0, 0] - size))
        i1 = int(round(coordinates[i, 0, 0] + size))
        j0 = int(round(coordinates[i, 0, 1] - size))
        j1 = int(round(coordinates[i, 0, 1] + size))
        if ((i0 >= 0) and (i1 >= 0) and (j0 >= 0) and (j1 >= 0) and
            (i0 < image.shape[1]) and (i1 < image.shape[1]) and
                (j0 < image.shape[0]) and (j1 < image.shape[0])):
            clip = image[j0:j1, i0:i1]
            sharpness = calculate_sharpness(clip)
            if sharpness < min_sharpness:
                blurry_corners.append(i)
        else:
            # we cannot calculate the sharpness in this way
            # this means, we do not know the sharpness
            blurry_corners.append(i)
    if len(blurry_corners) > 0:
        coordinates = numpy.delete(
            coordinates, blurry_corners, axis=0)
    log.debug(f'removed {len(blurry_corners)} blurry corners '
              f'(min_sharpness = {min_sharpness})')
    log.debug('removed %i blurry corners (min_sharpness = %f)',
              len(blurry_corners), min_sharpness)
    return coordinates
