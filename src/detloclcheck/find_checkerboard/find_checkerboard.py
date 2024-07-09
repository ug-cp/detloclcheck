"""
:mod:`detloclcheck.find_checkerboard.find_checkerboard`
=======================================================
:synopsis: :mod:`detloclcheck.find_checkerboard.find_checkerboard`
           provides the helper functions for
           :func:`detloclcheck.find_checkerboard.find_checkerboard`.
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

import itertools
import logging
import multiprocessing

import cv2
import numpy
from detloclcheck.tools import (calculate_square_distances,
                                filter_blurry_corners)

from .calculatetemplatematching import CalculateTemplateMatching
from .create_template import create_template
from .parallelfind4quadcornersubpix import ParallelFind4QuadCornerSubpix
from .set_black_border import _set_black_border


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
        _set_black_border(
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
    # filter blurry corners
    approx_coordinates = filter_blurry_corners(
        image, approx_coordinates, crosssizes[0], min_sharpness)
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
