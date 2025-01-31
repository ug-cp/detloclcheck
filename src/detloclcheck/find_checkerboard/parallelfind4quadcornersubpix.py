# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-08
:License: LGPL-3.0-or-later
:Copyright: (C) 2024 Daniel Mohr

.. currentmodule:: detloclcheck.find_checkerboard.parallelfind4quadcornersubpix
.. autoclass:: ParallelFind4QuadCornerSubpix
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
class ParallelFind4QuadCornerSubpix():
    """
    :Author: Daniel Mohr
    :Date: 2024-07-08
    :License: LGPL-3.0-or-later
    """
    def __init__(self, image, coordinates, window_size):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-01
        :License: LGPL-3.0-or-later

        ! :func:`cv2.find4QuadCornerSubpix` seems not to work        !
        ! and this :class:`ParallelFind4QuadCornerSubpix` is useless !

        runs :func:`cv2.find4QuadCornerSubpix` parallel using
        :mod:`multiprocessing`

        :param image: image of a checkerboard
        :param coordinates: approximated coordinates of the inner corners
        :param window_size: window size (length of a checkerboard field) to
                            do the optimization

        Example:

        >>> pfqs = ParallelFind4QuadCornerSubpix(
        ...     image, approx_coordinates, (window_size, window_size))
        >>> coordinates = pfqs()
        """
        self.image = image
        self.coordinates = coordinates
        self.window_size = window_size

    def __call__(self):
        iter_data = numpy.array_split(
            self.coordinates, multiprocessing.cpu_count())
        with multiprocessing.Pool() as pool:
            map_results = list(pool.map(self._fqs, iter_data))
        nretval = []
        ncorners = []
        for retval, corners in map_results:
            nretval.append(retval)
            ncorners.append(corners)
        results = [all(nretval), numpy.vstack(ncorners)]
        return results

    def _fqs(self, coordinates):
        return cv2.find4QuadCornerSubpix(
            self.image, coordinates, self.window_size)
