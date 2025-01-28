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

import numpy


def calculate_square_distances(x0, y0, x1, y1):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2018-02-12 (last change).
    :License: LGPL-3.0-or-later

    calculate the squared distances between all given
    points (x0,y0) and (x1,y1)

    :param x0: numpy array (vector) with the x coordinates in a column vector
    :param y0: numpy array (vector) with the y coordinates in a column vector
    :param x1: numpy array (vector) with the x coordinates in a column vector
    :param y1: numpy array (vector) with the y coordinates in a column vector

    :returns: return a matrix A with all squared distances
              A[i,j] is the distance between (x0[j],y0[j]) and (x1[i],y1[i])
    """
    # calculate x-distances
    # (numpy.ones((x1.shape[0],1)) * x0)
    # numpy.tile(x0,x1.shape[0]).reshape((x1.shape[0],x0.shape[0]))
    xd = ((numpy.ones((x1.shape[0], 1)) * x0) -
          (numpy.ones((x0.shape[0], 1)) * x1).transpose())
    # calculate y-distances
    yd = ((numpy.ones((y1.shape[0], 1)) * y0) -
          (numpy.ones((y0.shape[0], 1)) * y1).transpose())
    # calculate square of distances and return it
    return numpy.square(xd) + numpy.square(yd)
