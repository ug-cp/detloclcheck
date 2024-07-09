"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-09
:License: LGPL-3.0-or-later
:Copyright: (C) 2024 Daniel Mohr

.. currentmodule::
   detloclcheck.create_checkerboard_image.checkerboard_image_class
.. autofunction:: simpsons_rule
.. autoclass:: CheckerboardImageClass
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

import numpy
import scipy.integrate


def simpsons_rule(f, x1, x2, y1, y2):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2016-04-17
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    Integrate the function f over the area [x1,x2] x [y1,y2] by using
    Simpson's Rule.
    """
    x12 = (x1+x2)/2.0
    y12 = (y1+y2)/2.0
    s = numpy.zeros((9,), dtype=float)
    s[0] = f(x1, y1)
    s[1] = 4.0 * f(x12, y1)
    s[2] = f(x2, y1)
    s[3] = 4.0 * f(x1, y12)
    s[4] = 16.0 * f(x12, y12)
    s[5] = 4.0 * f(x2, y12)
    s[6] = f(x1, y2)
    s[7] = 4.0 * f(x12, y2)
    s[8] = f(x2, y2)
    # s.sort() # this is not significant better
    return (x2-x1) * (y2-y1) * s.sum() / 36.0


class CheckerboardImageClass():
    def __init__(self, size, zeropoint,
                 integrate_method=0, transition_value=128):
        """
        Example:

        from detloclcheck.create_checkerboard_image.checkerboard_image_class \
            import CheckerboardImageClass
        c = CheckerboardImageClass(1, (10,10), 0)
        c(0,0)
        c(0,0.5)
        c(0,1)
        """
        self.size = size
        self.zeropoint = numpy.array(zeropoint)
        self.integrate_method = integrate_method
        self.transition_value = transition_value

    def value(self, x, y):
        xy = (x, y)
        v = (xy - self.zeropoint) / self.size
        if (-2 <= v[1]) and (v[1] <= -1) and (-3 <= v[0]) and (v[0] <= 2):
            if ((-5/3 <= v[1]) and (v[1] <= -4/3) and
                    (-8/3 <= v[0]) and (v[0] <= 5/3)):
                return 255
        elif (-1 <= v[1]) and (v[1] <= 2) and (-2 <= v[0]) and (v[0] <= -1):
            if ((-2/3 <= v[1]) and (v[1] <= 5/3) and
                    (-5/3 <= v[0]) and (v[0] <= -4/3)):
                return 255
        elif (numpy.floor(v) == v).any():
            if (-2 <= v[1]) and (v[1] <= -1) and (-3 <= v[0]) and (v[0] <= 2):
                return 0
            if (-1 <= v[1]) and (v[1] <= 2) and (-2 <= v[0]) and (v[0] <= -1):
                return 0
            return self.transition_value
        elif int(numpy.sum(numpy.floor(v))) % 2 == 0:
            return 255
        return 0

    def __call__(self, x, y):
        if self.integrate_method == 0:
            return self.value(x, y)
        elif self.integrate_method == 1:
            return simpsons_rule(
                self.value,
                x - 0.5, x + 0.5,
                y - 0.5, y + 0.5)
        elif self.integrate_method == 2:
            v, _ = scipy.integrate.nquad(
                self.value, [[x - 0.5, x + 0.5], [y - 0.5, y + 0.5]])
            return v
