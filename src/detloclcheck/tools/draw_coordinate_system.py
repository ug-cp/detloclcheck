# SPDX-FileCopyrightText: 2024 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
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

import cv2
import numpy


def draw_coordinate_system(
        image, zeropoint, axis1, axis2, coordinate_system, factor=2):
    """
    :Author: Daniel Mohr
    :Email: ddaniel.mohr@uni-greifswald.de
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    ooimagescale = max(1, int(factor * 100/numpy.linalg.norm(axis1)))
    ooimage = cv2.cvtColor(
        cv2.resize(image,
                   (ooimagescale*image.shape[1], ooimagescale*image.shape[0]),
                   interpolation=cv2.INTER_AREA),
        cv2.COLOR_GRAY2BGR)
    lengthfactor1 = 1
    lengthfactor2 = 1
    for i in range(100):
        x = zeropoint + i*axis1
        if ((x[0] < 0) or (x[0] >= image.shape[1]) or
                (x[1] < 0) or (x[1] >= image.shape[0])):
            lengthfactor1 = max(1, i-1)
            break
    for i in range(100):
        x = zeropoint + i*axis2
        if ((x[0] < 0) or (x[0] >= image.shape[1]) or
                (x[1] < 0) or (x[1] >= image.shape[0])):
            lengthfactor2 = max(1, i-1)
            break
    cv2.arrowedLine(
        ooimage,
        numpy.round(ooimagescale * zeropoint).astype(int),
        numpy.round(ooimagescale * (
            zeropoint + lengthfactor1 * axis1)).astype(int),
        (0, 0, 255), factor * 7)  # red
    cv2.putText(
        ooimage,
        'x',
        numpy.round(ooimagescale * (
            zeropoint + max(0.5, lengthfactor1 - 1) * axis1)).astype(int),
        cv2.FONT_HERSHEY_SIMPLEX,
        factor * 3,  # fontScale
        (0, 0, 255),  # color
        factor * 7)  # thickness
    cv2.arrowedLine(
        ooimage,
        numpy.round(ooimagescale * zeropoint).astype(int),
        numpy.round(ooimagescale * (
            zeropoint + lengthfactor2 * axis2)).astype(int),
        (255, 0, 0), factor * 7)  # blue
    cv2.putText(
        ooimage,
        'y',
        numpy.round(ooimagescale * (
            zeropoint + max(0.5, lengthfactor2 - 1) * axis2)).astype(int),
        cv2.FONT_HERSHEY_SIMPLEX,
        factor * 3,  # fontScale
        (255, 0, 0),  # color
        factor * 7)  # thickness
    # mark corners
    for i in range(coordinate_system.shape[0]):
        cv2.putText(
            ooimage,
            f'({coordinate_system[i, 1, 0].astype(int)},'
            f'{coordinate_system[i, 1, 1].astype(int)})',
            (ooimagescale*coordinate_system[i, 0, :]).astype(int),
            cv2.FONT_HERSHEY_SIMPLEX,
            factor * 0.5,  # fontScale
            (0, 255, 0),  # color
            factor * 2)  # thickness
    return ooimage
