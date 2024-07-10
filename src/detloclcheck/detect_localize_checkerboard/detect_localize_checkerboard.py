"""
:mod:`detloclcheck.detect_localize_checkerboard.detect_localize_checkerboard`
=============================================================================
   :synopsis: :mod:`detloclcheck` is a python module for Detection and
              Localization of a Checkerboard calibration target containing
              L shape marker using template matching.
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

import logging

from detloclcheck.create_coordinate_system import create_coordinate_system
from detloclcheck.find_checkerboard import find_checkerboard
from detloclcheck.tools import filter_blurry_corners


def detect_localize_checkerboard(
        image, crosssizes, angles,
        hit_bound=0.93, min_sharpness=(100, 500, 1000), run_parallel=False,
        max_distance_factor_range=(
            1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.),
        log=None):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-10
    :License: LGPL-3.0-or-later

    Example:

    >>> from detloclcheck.create_checkerboard_image import \
    ...    create_checkerboard_image
    >>> image = create_checkerboard_image(8, 8, 15)
    >>> from detloclcheck.detect_localize_checkerboard import \
    ...    detect_localize_checkerboard
    >>> coordinate_system, zeropoint, axis1, axis2 = \
    ...    detect_localize_checkerboard(\
    ...        image, crosssizes=(11,),\
    ...        angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))
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
        return 1
    # filter blurry corners (2)
    coordinates = filter_blurry_corners(
        image, coordinates, crosssizes[0], min_sharpness[1])
    if coordinates.shape[0] < 24:
        log.error(
            'ERROR: only %i corners detected, '
            'but we need at least 24 for marker detection',
            coordinates.shape[0])
        return 1
    log.debug(f'go on with {coordinates.shape[0]} corners')
    coordinate_system, zeropoint, axis1, axis2 = create_coordinate_system(
        image, coordinates, max_distance_factor_range,
        min_sharpness=min_sharpness[2])
    if coordinate_system is None:
        return zeropoint  # zeropoint is used as error code
    return coordinate_system, zeropoint, axis1, axis2
