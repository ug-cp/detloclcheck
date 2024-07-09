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


def normed_TM_CCORR_NORMED(image, template):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de, daniel.mohr@uni-greifswald.de
    :Date: 2018-02-14, 2024-06-12 (last change).
    :License: LGPL-3.0-or-later
    """
    mapimage = numpy.zeros(image.shape, dtype=numpy.float32)
    y0 = template.shape[0] // 2
    x0 = template.shape[1] // 2
    y1 = y0 + image.shape[0] - (template.shape[0] - 1)
    x1 = x0 + image.shape[1] - (template.shape[1] - 1)
    mapimage[y0:y1, x0:x1] = \
        0.5 * (1.0 + cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED))
    return mapimage
