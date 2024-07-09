"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-08
:License: LGPL-3.0-or-later
:Copyright: (C) 2024 Daniel Mohr

.. currentmodule:: detloclcheck.find_checkerboard.create_template
.. autofunction:: create_template
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

import functools

import numpy


@functools.cache
def create_template(crosssize):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    template = numpy.zeros((crosssize, crosssize), dtype=numpy.uint8)
    numpy.fill_diagonal(template, 128)
    numpy.fill_diagonal(numpy.fliplr(template), 128)
    for i in range(crosssize):
        template[i, (1+i):(crosssize-i-1)] = 255
        template[i, (crosssize-i):i] = 255
    return template
