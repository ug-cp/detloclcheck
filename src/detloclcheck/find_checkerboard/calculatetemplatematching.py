# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-08
:License: LGPL-3.0-or-later
:Copyright: (C) 2024 Daniel Mohr

.. currentmodule:: detloclcheck.find_checkerboard.calculatetemplatematching
.. autofunction:: _rotate_image
.. autofunction:: _get_map

.. autoclass:: CalculateTemplateMatching
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

import cv2
import numpy
from detloclcheck.tools import normed_tm_ccorr_normed

from .create_template import create_template


def _rotate_image(image, angle):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-11, 2024-06-13
    :License: LGPL-3.0-or-later

    rotate a gray image by an angle
    """
    (height, width) = image.shape
    rotate_center = (width / 2, height / 2)
    transformation_matrix = cv2.getRotationMatrix2D(rotate_center, angle, 1)
    return cv2.warpAffine(image, transformation_matrix, (width, height))


def _get_map(image, crosssize, angle):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    template = create_template(crosssize)
    if angle == 0:
        result = normed_tm_ccorr_normed(image, template)
    else:
        diagonal = int(numpy.linalg.norm(image.shape))
        pos = ((diagonal - image.shape[0]) // 2,
               (diagonal - image.shape[1]) // 2)
        large_image = numpy.zeros((diagonal, diagonal), dtype=numpy.uint8)
        large_image[pos[0]:pos[0] + image.shape[0],
                    pos[1]:pos[1] + image.shape[1]] = image
        rotated_image = _rotate_image(large_image, angle)
        template_map = normed_tm_ccorr_normed(rotated_image, template)
        unrotated_image = _rotate_image(template_map, -angle)
        result = unrotated_image[
            pos[0]:pos[0] + image.shape[0],
            pos[1]:pos[1] + image.shape[1]]
    # from detloclcheck.tools import array2image
    # cv2.imwrite('template.png', array2image(template))
    return result


# pylint: disable=too-few-public-methods
class CalculateTemplateMatching():
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    def __init__(self, image):
        self.image = image

    def __call__(self, crosssize_angle):
        crosssize, angle = crosssize_angle
        return _get_map(self.image, crosssize, angle)
