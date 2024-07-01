"""
:mod:`detloclcheck.find_checkerboard.find_checkerboard`
=======================================================
:synopsis: :mod:`detloclcheck.find_checkerboard.find_checkerboard`
           provides the helper functions for
           :func:`detloclcheck.find_checkerboard.find_checkerboard`.
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-01
:License: LGPL-3.0-or-later
:Copyright: (C) 2024 Daniel Mohr

.. currentmodule:: detloclcheck.find_checkerboard.find_checkerboard
.. autofunction:: create_template
.. autofunction:: array2image
.. autofunction:: rotate
.. autofunction:: _normed_TM_CCORR_NORMED
.. autofunction:: get_map
.. autofunction:: set_black_border
.. autofunction:: calculate_square_distances
.. autofunction:: calculate_sharpness

.. autoclass:: CalculateTemplateMatching
   :members:
   :private-members:
   :special-members:

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

import functools
import itertools
import logging
import multiprocessing

import cv2
import numpy


@functools.cache
def create_template(crosssize):
    template = numpy.zeros((crosssize, crosssize), dtype=numpy.uint8)
    numpy.fill_diagonal(template, 128)
    numpy.fill_diagonal(numpy.fliplr(template), 128)
    for i in range(crosssize):
        template[i, (1+i):(crosssize-i-1)] = 255
        template[i, (crosssize-i):i] = 255
    return template


def array2image(a):
    return cv2.normalize(
        a, None, alpha=0, beta=255,
        norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)


def rotate(image, angle):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-11, 2024-06-13
    :License: LGPL-3.0-or-later

    rotate a gray image by an angle
    """
    (height, width) = image.shape
    rotate_center = (width / 2, height / 2)
    M = cv2.getRotationMatrix2D(rotate_center, angle, 1)
    return cv2.warpAffine(image, M, (width, height))


def _normed_TM_CCORR_NORMED(image, template):
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


def get_map(image, crosssize, angle):
    template = create_template(crosssize)
    if angle == 0:
        result = _normed_TM_CCORR_NORMED(image, template)
    else:
        diagonal = int(numpy.linalg.norm(image.shape))
        pos = ((diagonal - image.shape[0]) // 2,
               (diagonal - image.shape[1]) // 2)
        large_image = numpy.zeros((diagonal, diagonal), dtype=numpy.uint8)
        large_image[pos[0]:pos[0] + image.shape[0],
                    pos[1]:pos[1] + image.shape[1]] = image
        rotated_image = rotate(large_image, angle)
        template_map = _normed_TM_CCORR_NORMED(rotated_image, template)
        unrotated_image = rotate(template_map, -angle)
        result = unrotated_image[
            pos[0]:pos[0] + image.shape[0],
            pos[1]:pos[1] + image.shape[1]]
    cv2.imwrite('template.png', array2image(template))
    return result


class CalculateTemplateMatching():
    def __init__(self, image):
        self.image = image

    def __call__(self, crosssize_angle):
        crosssize, angle = crosssize_angle
        return get_map(self.image, crosssize, angle)


def set_black_border(image, templateshape):
    border_size = templateshape[0] // 2
    image[:border_size, :] = 0
    image[-border_size:, :] = 0
    border_size = templateshape[1] // 2
    image[:, :border_size] = 0
    image[:, -border_size:] = 0


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


def calculate_sharpness(img):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@uni-greifswald.de
    :Date: 2024-02-20
    :License: LGPL-3.0-or-later
    """
    return cv2.Laplacian(img, cv2.IMREAD_GRAYSCALE).var()


class ParallelFind4QuadCornerSubpix():
    def __init__(self, image, coordinates, window_size):
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


def find_checkerboard(
        image, crosssizes=None, angles=None,
        hit_bound=0.93, min_sharpness=100, run_parallel=False):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later

    find the inner checkerboard corners in the image

    :param image: 2 dimensional numpy array describing the image
    :param crosssizes: list of cross sizes to test
    :param angles: list of angles to test
    :param hit_bound: minimal value in the template matching to be a
                      checkerboard corner
    :param min_sharpness: minimal sharpness for a good corner

    """
    log = logging.getLogger('detloclcheck.find_checkerboard')
    if crosssizes is None:
        crosssizes = [5, 11, 23]
    if angles is None:
        angles = [0, 45, 90, 135]
    _ = map(create_template, crosssizes)
    iter_data = itertools.product(crosssizes, angles)
    calculate_template_matching = CalculateTemplateMatching(image)
    if run_parallel:
        with multiprocessing.Pool() as pool:
            template_machting_maps = list(
                pool.map(calculate_template_matching, iter_data))
    else:
        template_machting_maps = list(
            map(calculate_template_matching, iter_data))
    max_crosssize = max(crosssizes)
    for template_machting_map in template_machting_maps:
        set_black_border(
            template_machting_map, (max_crosssize, max_crosssize))
    overall_map = numpy.zeros(
        image.shape, dtype=template_machting_maps[0].dtype)
    for template_machting_map in template_machting_maps:
        overall_map = numpy.maximum(overall_map, template_machting_map)
    log.debug('found template matching maps')
    approx_coordinates = []
    mask = numpy.ones(overall_map.shape, dtype=numpy.uint8)
    window_half_size = max(crosssizes) // 2
    mask[0:(window_half_size+1), :] = 0
    mask[-(window_half_size+2):, :] = 0
    mask[:, 0:(window_half_size+1)] = 0
    mask[:, -(window_half_size+2):] = 0
    while True:
        _, maxval, _, pos = cv2.minMaxLoc(overall_map, mask)
        if maxval >= hit_bound:  # check if pos could be a chessboard corner
            approx_coordinates.append(numpy.array([pos], dtype=numpy.float32))
            y0 = pos[1] - window_half_size
            y1 = pos[1] + window_half_size + 1
            x0 = pos[0] - window_half_size
            x1 = pos[0] + window_half_size + 1
            mask[y0:y1, x0:x1] = 0
        else:
            break
    approx_coordinates = numpy.array(approx_coordinates)
    log.debug('found approximated coordinates')
    # filter blurry corners (1)
    blurry_corners = []
    size = crosssizes[0]
    log.debug(f'use size = {size} for filtering blurry corners')
    for i in range(approx_coordinates.shape[0]):
        i0 = int(round(approx_coordinates[i, 0, 0] - size))
        i1 = int(round(approx_coordinates[i, 0, 0] + size))
        j0 = int(round(approx_coordinates[i, 0, 1] - size))
        j1 = int(round(approx_coordinates[i, 0, 1] + size))
        if ((i0 >= 0) and (i1 >= 0) and (j0 >= 0) and (j1 >= 0) and
            (i0 < image.shape[1]) and (i1 < image.shape[1]) and
                (j0 < image.shape[0]) and (j1 < image.shape[0])):
            clip = image[j0:j1, i0:i1]
            sharpness = calculate_sharpness(clip)
            if sharpness < min_sharpness:
                blurry_corners.append(i)
        else:
            # we cannot calculate the sharpness in this way
            # this means, we do not know the sharpness
            blurry_corners.append(i)
    if len(blurry_corners) > 0:
        approx_coordinates = numpy.delete(
            approx_coordinates, blurry_corners, axis=0)
    log.debug(f'removed {len(blurry_corners)} blurry corners')
    n = approx_coordinates.shape[0]
    distances = calculate_square_distances(
        approx_coordinates[:, :, 0].reshape((n,)),
        approx_coordinates[:, :, 1].reshape((n,)),
        approx_coordinates[:, :, 0].reshape((n,)),
        approx_coordinates[:, :, 1].reshape((n,)))
    numpy.fill_diagonal(distances, numpy.inf)  # ignore 0 distances
    minimal_distance = numpy.sqrt(distances.min())
    window_size = int(0.75 * minimal_distance)
    # window_size has to be small to fit in image around coordinates
    window_size = int(min(
        window_size, approx_coordinates.min(),
        image.shape[1] - approx_coordinates[:, :, 0].max(),
        image.shape[0] - approx_coordinates[:, :, 1].max()))
    log.debug('window_size calculated')
    pfqs = ParallelFind4QuadCornerSubpix(
        image, approx_coordinates, (window_size, window_size))
    coordinates = pfqs()
    log.debug(f'found {coordinates[1].shape[0]} corners')
    if coordinates[0]:
        return coordinates[1]
    else:
        return None
