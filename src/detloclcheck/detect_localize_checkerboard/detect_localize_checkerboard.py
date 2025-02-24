# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:mod:`detloclcheck.detect_localize_checkerboard.detect_localize_checkerboard`
=============================================================================
   :synopsis: :mod:`detloclcheck` is a python module for Detection and
              Localization of a Checkerboard calibration target containing
              L shape marker using template matching.
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-02-24
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

import logging

from detloclcheck.create_coordinate_system import create_coordinate_system
from detloclcheck.find_checkerboard import find_checkerboard
from detloclcheck.tools import filter_blurry_corners


def detect_localize_checkerboard(
        image, crosssizes, angles, *,
        hit_bound=0.93, min_sharpness=(100, 500, 1000), run_parallel=False,
        max_distance_factor_range=(
            1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.),
        log=None):
    """
    :Author: Daniel Mohr
    :Date: 2025-02-24
    :License: LGPL-3.0-or-later

    Detect and localize a checkerboard in an image.

    :param image: numpy array, the input image
    :param crosssizes: tuple, size of the crosses in the checkerboard
    :param angles: tuple, a guess of the angle(s) of the crosses
                   in the checkerboard
    :param hit_bound: the hit bound
    :param min_sharpness: tuple, the minimum sharpness at different steps.
                          The first low values allow detection of the
                          zero point, and the last value defines which
                          crosses should be used in the end.
    :param run_parallel: whether to run the detection in parallel
    :param max_distance_factor_range: the maximum distance factor range
    :param log: a logger instance

    :return: (coordinate_system, zeropoint, axis1, axis2) on success,
             otherwise (None, error_code, None, None).
             possible error codes: 1, 2, 3, 4, 5, 6, 7
    Notes:
    This function uses :func:`detloclcheck.find_checkerboard.find_checkerboard` 
    to detect the checkerboard and then
    :func:`detloclcheck.tools.filter_blurry_corners` 
    to filter out blurry corners. Finally, :func:`create_coordinate_system` 
    is used to obtain the world coordinates.

    Example 1:

    >>> from detloclcheck.create_checkerboard_image import \
    ...    create_checkerboard_image
    >>> _, _, image = create_checkerboard_image(8, 8, 15)
    >>> from detloclcheck.detect_localize_checkerboard import \
    ...    detect_localize_checkerboard
    >>> coordinate_system, zeropoint, axis1, axis2 = \
    ...    detect_localize_checkerboard(\
    ...        image, crosssizes=(11,),\
    ...        angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))

    Example 2:

    >>> import cv2
    >>> from detloclcheck import find_checkerboard
    >>> image = cv2.imread('foo.png')
    >>> gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    >>> from detloclcheck.detect_localize_checkerboard import \
    ...     detect_localize_checkerboard
    >>> coordinate_system, zeropoint, axis1, axis2 = \
    ...     detect_localize_checkerboard(
    ...         gray_image, (35,55), (0, 45, 90, 135),
    ...         min_sharpness=(25, 50, 100))
    >>> import matplotlib.pyplot
    >>> matplotlib.pyplot.imshow(gray_image, cmap="Greys")
    >>> matplotlib.pyplot.plot(
    ...     coordinate_system[:, 0, 0], coordinate_system[:, 0, 1],
    ...     'r1', markersize=20)
    >>> matplotlib.pyplot.show()
    """
    if log is None:
        log = logging.getLogger('detloclcheck')
    coordinates = find_checkerboard(
        image,
        crosssizes=crosssizes,
        angles=angles,
        hit_bound=hit_bound,
        min_sharpness=min_sharpness[0],
        run_parallel=run_parallel)
    if coordinates is None:
        log.error('ERROR: no inner corners detected')
        return None, 1, None, None
    # filter blurry corners (2)
    coordinates = filter_blurry_corners(
        image, coordinates, crosssizes[0], min_sharpness[1])
    if coordinates.shape[0] < 24:
        log.error(
            'ERROR: only %i corners detected, '
            'but we need at least 24 for marker detection',
            coordinates.shape[0])
        return None, 7, None, None
    log.debug('go on with %i corners', coordinates.shape[0])
    coordinate_system, zeropoint, axis1, axis2 = create_coordinate_system(
        image, coordinates, max_distance_factor_range,
        min_sharpness=min_sharpness[2])
    return coordinate_system, zeropoint, axis1, axis2
