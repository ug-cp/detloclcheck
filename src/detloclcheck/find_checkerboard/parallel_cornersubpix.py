# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-01-29
:License: LGPL-3.0-or-later
:Copyright: (C) 2024, 2025 Daniel Mohr

.. currentmodule:: detloclcheck.find_checkerboard.parallel_cornersubpix
.. autoclass:: ParallelCornerSubPix
   :members:
   :private-members:
   :special-members:

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

import multiprocessing

import cv2
import numpy


# pylint: disable=too-few-public-methods
class ParallelCornerSubPix():
    """
    :Author: Daniel Mohr
    :Date: 2025-01-29
    :License: LGPL-3.0-or-later
    """
    def __init__(self, image, coordinates, window_size,
                 zero_zone=(-1, -1),
                 criteria_max_count=42,
                 criteria_epsilon=0.001):
        """
        :Author: Daniel Mohr
        :Date: 2025-01-29
        :License: LGPL-3.0-or-later

        runs :func:`cv2.cornerSubPix` parallel using
        :mod:`multiprocessing`

        :param image: image of a checkerboard
        :param coordinates: approximated coordinates of the inner corners
        :param window_size: window size (half of the length of a checkerboard
                            field) to do the optimization
        :param zero_zone: parameter for :func:`cv2.cornerSubPix`
                          to define a region which should not be used
                          (avoid possible singularities by autocorrelation)
        :param criteria_max_count: parameter for :func:`cv2.cornerSubPix`
                                   to define the maximal count of iterations
        :param criteria_epsilon: parameter for :func:`cv2.cornerSubPix` to
                                 minimal corner position move between 2 steps

        Example:

        >>> pfcsp = ParallelCornerSubPix(
        ...     image, approx_coordinates, (window_size, window_size))
        >>> coordinates = pfcsp()
        """
        self.image = image
        self.coordinates = coordinates
        self.window_size = window_size
        self.zero_zone = zero_zone
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_COUNT,
                         criteria_max_count, criteria_epsilon)

    def __call__(self):
        iter_data = numpy.array_split(
            self.coordinates, multiprocessing.cpu_count())
        with multiprocessing.Pool() as pool:
            map_results = list(pool.map(self._fqs, iter_data))
        ncorners = []
        for corners in map_results:
            ncorners.append(corners)
        results = numpy.vstack(ncorners)
        return results

    def _fqs(self, coordinates):
        return cv2.cornerSubPix(
            self.image, coordinates, self.window_size,
            self.zero_zone, self.criteria)
