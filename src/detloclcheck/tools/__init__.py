# SPDX-FileCopyrightText: 2024 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:mod:`detloclcheck.tools`
=========================
   :synopsis: :mod:`detloclcheck` is a python module for Detection and
              Localization of a Checkerboard calibration target containing
              L-shape marker using template matching.

.. contents::

description
-----------

`DetLocLCheck` is a software tool for Detection and Localization of a
Checkerboard calibration target containing L-shape marker using
template matching.

functions
---------
.. currentmodule:: detloclcheck.tools
.. autofunction:: array2image
.. autofunction:: calculate_sharpness
.. autofunction:: calculate_square_distances
.. autofunction:: draw_coordinate_system
.. autofunction:: filter_blurry_corners
.. autofunction:: normed_tm_ccorr_normed

copyright + license
-------------------
:Author: Daniel Mohr
:Date: 2024-07-08
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

from .array2image import array2image
from .calculate_sharpness import calculate_sharpness
from .calculate_square_distances import calculate_square_distances
from .draw_coordinate_system import draw_coordinate_system
from .filter_blurry_corners import filter_blurry_corners
from .normed_tm_ccorr_normed import normed_tm_ccorr_normed

__all__ = ["array2image",
           "calculate_sharpness",
           "calculate_square_distances",
           "draw_coordinate_system",
           "filter_blurry_corners",
           "normed_tm_ccorr_normed"]
