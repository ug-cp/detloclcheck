# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-01-28
:License: LGPL-3.0-or-later
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

import logging

import cv2
import numpy
from detloclcheck.tools import (array2image, draw_coordinate_system,
                                filter_blurry_corners, normed_tm_ccorr_normed)


def _cal_coordinate_system(coordinates, zeropoint, axis1, axis2):
    coordinate_system = numpy.zeros((coordinates.shape[0], 2, 2))
    coordinate_system[:, 0, :] = coordinates[:, 0, :]
    A = numpy.vstack((axis1, axis2)).transpose()
    for i in range(coordinates.shape[0]):
        b = coordinates[i, 0, :] - zeropoint
        coordinate_system[i, 1, :] = numpy.linalg.solve(A, b).round()
    return coordinate_system


def _find_better_axis(
        coordinates, zeropoint, axis1, axis2, objectpoint, factor=1):
    if objectpoint[1] == 0:
        # zeropoint[0] + (1 0) * naxis = coordinates[?, 0, 0]
        # zeropoint[1] + (0 1) * naxis = coordinates[?, 0, 1]
        # zeropoint[0] + (2 0) * naxis = coordinates[?, 0, 0]
        # zeropoint[1] + (0 2) * naxis = coordinates[?, 0, 1]
        coordinate_system = _cal_coordinate_system(
            coordinates, zeropoint, axis1, axis2)
        indizes = [None] * max(objectpoint)
        A = numpy.zeros((2 * max(objectpoint), 2))
        b = numpy.zeros((2 * max(objectpoint), ))
        for j in range(1, 1+max(objectpoint)):
            objctpnt = (j, 0)
            index = None
            for i in range(coordinates.shape[0]):
                if (coordinate_system[i, 1, :] == objctpnt).all():
                    index = i
                    break
            if index is not None:
                indizes[j-1] = index
                A[2*(j-1):2*(j-1)+2, :] = j * numpy.eye(2)
                b[2*(j-1):2*(j-1)+2] = coordinates[index, 0, :] - zeropoint
        new_axis, residuals, rank, s = numpy.linalg.lstsq(A, b, rcond=None)
        if (rank == 0) or (residuals[0] > 1):
            new_axis = None
    else:
        # zeropoint[0] + (1 0) * naxis = coordinates[?, 0, 0]
        # zeropoint[1] + (0 1) * naxis = coordinates[?, 0, 1]
        # zeropoint[0] + (2 0) * naxis = coordinates[?, 0, 0]
        # zeropoint[1] + (0 2) * naxis = coordinates[?, 0, 1]
        coordinate_system = _cal_coordinate_system(
            coordinates, zeropoint, axis1, axis2)
        indizes = [None] * max(objectpoint)
        A = numpy.zeros((2 * max(objectpoint), 2))
        b = numpy.zeros((2 * max(objectpoint), ))
        for j in range(1, 1+max(objectpoint)):
            objctpnt = (0, j)
            index = None
            for i in range(coordinates.shape[0]):
                if (coordinate_system[i, 1, :] == objctpnt).all():
                    index = i
                    break
            if index is not None:
                indizes[j-1] = index
                A[2*(j-1):2*(j-1)+2, :] = j * numpy.eye(2)
                b[2*(j-1):2*(j-1)+2] = coordinates[index, 0, :] - zeropoint
        if max(objectpoint) > 1:
            new_axis, residuals, rank, s = numpy.linalg.lstsq(A, b, rcond=None)
        else:
            try:
                new_axis = numpy.linalg.solve(A, b)
                residuals = [0]
                rank = 2
            except numpy.linalg.LinAlgError:
                new_axis = None
        if (new_axis is not None) and ((rank == 0) or (residuals[0] > 1)):
            new_axis = None
    return new_axis


def calculate_square_distances(x0, y0, x1, y1):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2018-02-12 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

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


def create_coordinate_system(
        image, coordinates, max_distance_factor_range, min_sharpness=1000,
        draw_images=(False, False, False)):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@uni-greifswald.de
    :Date: 2025-01-28 (last change).

    :param image: 2 dimensional numpy array describing the image
    :param coordinates: numpy array with the coordinates of the corners;
                        could be returned from
                        :func:`detloclcheck.find_checkerboardfind_checkerboard`

    :return: (coordinate_system, zeropoint, axis1, axis2) on success,
             otherwise (None, error_code, None, None).
             possible error codes: 2, 3, 4, 5, 6
    """
    log = logging.getLogger('detloclcheck.create_coordinate_system')
    centerpoint = 0.5 * numpy.array(image.shape)
    n = coordinates.shape[0]
    distances = \
        (coordinates[:, :, 0].reshape((n,)) - centerpoint[1])**2 + \
        (coordinates[:, :, 1].reshape((n,)) - centerpoint[0])**2
    axis1 = None
    for max_distance_factor in max_distance_factor_range:
        rel_distance_interval = (
            1/max_distance_factor, max_distance_factor)
        tmp_distances = distances.copy()
        while True:
            index = tmp_distances.argmin()
            if index == tmp_distances.argmax():
                break
            distances_to_index = \
                (coordinates[:, 0, 0].reshape((n,)) -
                 coordinates[index, 0, 0])**2 + \
                (coordinates[:, 0, 1].reshape((n,)) -
                 coordinates[index, 0, 1])**2
            distances_to_index.sort()
            axis1dist = distances_to_index[1:5] / distances_to_index[1]
            axisdist_ok = (
                (rel_distance_interval[0] < axis1dist[1:5]).all() and
                (axis1dist[1:5] < rel_distance_interval[1]).all())
            if axisdist_ok:
                # print('good', axis1dist[1:5], 'in', rel_distance_interval)
                distances_to_index = \
                    (coordinates[:, :, 0].reshape((n,)) -
                     coordinates[index, 0, 0])**2 + \
                    (coordinates[:, :, 1].reshape((n,)) -
                     coordinates[index, 0, 1])**2
                distances_to_index[index] = numpy.inf
                k = index
                j = distances_to_index.argmin()
                zeropoint = coordinates[k, :, :].reshape((2,))
                zeropoint_index = k
                log.debug(f'zeropoint {zeropoint}')
                axis1 = (coordinates[j, :, :] -
                         coordinates[k, :, :]).reshape((2,))
                if ((zeropoint + axis1 <= 0).any() or
                        (zeropoint + axis1 >= image.shape).any()):
                    axis1 = -axis1
                log.debug(f'axis1: |{axis1}| = {numpy.linalg.norm(axis1)}')
                break
            # print('bad', axis1dist[1:5], 'not in', rel_distance_interval)
            tmp_distances[index] = numpy.inf
        if axis1 is not None:
            break
    if axis1 is None:
        log.error('ERROR: no axis found')
        return None, 2, None, None
    log.debug('found first axis')

    # now we have found 1 axis; we do not know wheather it is x or y
    # and we do not know the direction
    # axis1 is only from a short distance. It should be enhanced:
    enhanced_axis1 = 1
    enhanced_axis2 = 0
    zeropoint_search_index = 0
    axis2 = numpy.dot(numpy.array([[0, -1], [1, 0]]), axis1)
    log.debug(f'actual axis: |{axis1}| = {numpy.linalg.norm(axis1)}, '
              f'|{axis2}| = {numpy.linalg.norm(axis2)}')
    while True:
        # now we have the other axis
        # we know:
        # (0,0) <-> zeropoint <-> coordinates[k, :, :]
        # (1,0) <-> coordinates[j, :, :]
        # now find (0, 1) and get a better axis2
        res = _find_better_axis(coordinates, zeropoint, axis1, axis2, (0, 1))
        if res is not None:
            axis2 = res
            log.debug(f'better axis2: |{axis2}| = {numpy.linalg.norm(axis2)}')
            enhanced_axis2 += 1
        # now find a better axis1 and axis2
        # for i in range(2, 7):
        for i in range(2, 4):
            not_found = 0
            res = _find_better_axis(
                coordinates, zeropoint, axis1, axis2, (i, 0), 1.0/i)
            if res is not None:
                axis1 = res
                log.debug(f'better axis1 ({i}): '
                          f'|{axis1}| = {numpy.linalg.norm(axis1)}')
                enhanced_axis1 += 1
            else:
                not_found += 1
            res = _find_better_axis(
                coordinates, zeropoint, axis1, axis2, (0, i), 1.0/i)
            if res is not None:
                axis2 = res
                log.debug(f'better axis2 ({i}): '
                          f'|{axis2}| = {numpy.linalg.norm(axis1)}')
                enhanced_axis2 += 1
            else:
                not_found += 1
            if not_found == 2:
                break
        if (enhanced_axis1 < 3) or (enhanced_axis2 < 3):
            # try another zeropoint
            log.debug(
                f'try another zeropoint ({enhanced_axis1}, {enhanced_axis2})')
            zeropoint = \
                coordinates[zeropoint_search_index, :, :].reshape((2,))
            zeropoint_index = zeropoint_search_index
            zeropoint_search_index += 1
            if zeropoint_search_index >= coordinates.shape[0]:
                # we have tried all corners as zeropoint
                log.error('ERROR: no good axis found (tried all corners)')
                return None, 3, None, None
            if ((zeropoint + axis1 <= 0).any() or
                    (zeropoint + axis1 >= image.shape).any()):
                axis1 = -axis1
                axis2 = numpy.dot(numpy.array([[0, -1], [1, 0]]), axis1)
            enhanced_axis1 = 1
            enhanced_axis2 = 0
        else:
            break
    coordinate_system = numpy.zeros((coordinates.shape[0], 2, 2))
    # coordinate_system[:, 0, :] are the pixel coordinates
    # coordinate_system[:, 1, :] are the coordinates in an artificial system
    coordinate_system[:, 0, :] = coordinates[:, 0, :]
    n = coordinate_system.shape[0]
    unassigned_indizes = list(range(n))
    unassigned_indizes.remove(zeropoint_index)
    assigned_indizes = [zeropoint_index]
    distances = calculate_square_distances(
        coordinate_system[:, 0, 0].reshape((n,)),
        coordinate_system[:, 0, 1].reshape((n,)),
        coordinate_system[:, 0, 0].reshape((n,)),
        coordinate_system[:, 0, 1].reshape((n,)))
    distances[:, zeropoint_index] = numpy.inf
    numpy.fill_diagonal(distances, numpy.inf)  # ignore known 0 distances
    A = numpy.vstack((axis1, axis2)).transpose()
    while len(unassigned_indizes) > 0:
        distances_to_assigend = distances[assigned_indizes, :]
        assigend_index, unassigned_index = numpy.unravel_index(
            distances_to_assigend.argmin(), distances_to_assigend.shape)
        assigend_index = assigned_indizes[assigend_index]
        b = coordinates[unassigned_index, 0, :] - \
            coordinates[assigend_index, 0, :]
        ij = coordinate_system[assigend_index, 1, :] + \
            numpy.linalg.solve(A, b).round()
        coordinate_system[unassigned_index, 1, :] = ij
        assigned_indizes.append(unassigned_index)
        unassigned_indizes.remove(unassigned_index)
        distances[:, unassigned_index] = numpy.inf
    if draw_images[0]:
        # draw coordinate system
        t_coordinate_system = coordinate_system.copy()
        t_coordinate_system[:, 1, 0] -= coordinate_system[:, 1, 0].min()
        t_coordinate_system[:, 1, 1] -= coordinate_system[:, 1, 1].min()
        cv2.imwrite(
            'oo.png',
            array2image(draw_coordinate_system(
                image, zeropoint, axis1, axis2, t_coordinate_system)))
    # now we have a preliminary coordinate system found
    # now we need to put the origin to the marker
    coordinatesmap = numpy.zeros(
        ((1 + coordinate_system[:, 1, 1].max().astype(int) -
          coordinate_system[:, 1, 1].min().astype(int)),
         (1 + coordinate_system[:, 1, 0].max().astype(int) -
          coordinate_system[:, 1, 0].min().astype(int))),
        dtype=numpy.uint8)
    coordinatesmap[
        (coordinate_system[:, 1, 1].astype(int) -
         coordinate_system[:, 1, 1].min().astype(int)),
        (coordinate_system[:, 1, 0].astype(int) -
         coordinate_system[:, 1, 0].min().astype(int))] = 255
    markertemplate = numpy.array(
        [[255, 255, 255, 255, 255, 255],
         [255,   0,   0, 255, 255, 255],
         [255,   0,   0, 255, 255, 255],
         [255,   0,   0,   0,   0, 255],
         [255,   0,   0,   0,   0, 255],
         [255, 255, 255, 255, 255, 255]], dtype=numpy.uint8)
    markerdirection = 'L'
    if ((coordinatesmap.shape[0] < markertemplate.shape[0]) or
            (coordinatesmap.shape[1] < markertemplate.shape[1])):
        # coordinatesmap is too small!
        return None, 6, None, None
    result = normed_tm_ccorr_normed(coordinatesmap, markertemplate)
    if result.max() != 1:
        act_markertemplate = numpy.fliplr(markertemplate)
        markerdirection = 'L fliplr'
        result = normed_tm_ccorr_normed(coordinatesmap, act_markertemplate)
        # print('result', result.max())
        if result.max() != 1:
            act_markertemplate = numpy.flipud(markertemplate)
            markerdirection = 'L flipud'
            result = normed_tm_ccorr_normed(coordinatesmap, act_markertemplate)
            if result.max() != 1:
                act_markertemplate = numpy.flipud(numpy.fliplr(markertemplate))
                markerdirection = 'L flipud fliplr'
                result = normed_tm_ccorr_normed(
                    coordinatesmap, act_markertemplate)
    if result.max() == 1:
        # marker exact found
        i, j = numpy.unravel_index(result.argmax(), result.shape)
        log.debug(
            f'preliminary marker found at ({j},{i}) with {markerdirection}')
        if markerdirection == 'L fliplr':
            i += coordinate_system[:, 1, 1].min().astype(int) - 1
            j += coordinate_system[:, 1, 0].min().astype(int) - 1
        elif markerdirection == 'L flipud':
            i += coordinate_system[:, 1, 1].min().astype(int)
            j += coordinate_system[:, 1, 0].min().astype(int)
        elif markerdirection == 'L flipud fliplr':
            i += coordinate_system[:, 1, 1].min().astype(int)
            j += coordinate_system[:, 1, 0].min().astype(int) - 1
        elif markerdirection == 'L':
            i += coordinate_system[:, 1, 1].min().astype(int) - 1
            j += coordinate_system[:, 1, 0].min().astype(int)
        else:
            # this should not happen
            log.error('ERROR')
            return None, 4, None, None
        log.debug(f'marker found at ({j},{i}) with {markerdirection}')
        # adapt coordinate system
        for k in range(coordinate_system.shape[0]):
            if ((coordinate_system[k, 1, 1] == i) and
                    (coordinate_system[k, 1, 0] == j)):
                zeropoint = coordinate_system[k, 0, :].reshape((2,))
                break
        coordinate_system[:, 1, 1] -= i
        coordinate_system[:, 1, 0] -= j
        # now we have to decide which one is x and which one is y
        # the longer marker bar shows in y direction
        angle = numpy.arctan2(axis2[1], axis2[0]) * 180 / numpy.pi
        rotate_center = tuple(zeropoint)
        clip_half_length = 4.5*numpy.linalg.norm(axis1)
        i0 = int(round(zeropoint[1]-clip_half_length))
        i1 = int(round(zeropoint[1]+clip_half_length))
        j0 = int(round(zeropoint[0]-clip_half_length))
        j1 = int(round(zeropoint[0]+clip_half_length))
        clip_image = image[i0:(1+i1), j0:(1+j1)]
        diagonal = int(numpy.linalg.norm(clip_image.shape))
        pos = ((diagonal - clip_image.shape[0]) // 2,
               (diagonal - clip_image.shape[1]) // 2)
        large_image = numpy.zeros((diagonal, diagonal), dtype=numpy.uint8)
        large_image[pos[0]:pos[0] + clip_image.shape[0],
                    pos[1]:pos[1] + clip_image.shape[1]] = clip_image
        (height, width) = large_image.shape
        rotate_center = (width / 2, height / 2)
        M = cv2.getRotationMatrix2D(rotate_center, angle, 1)
        rotated_image = cv2.warpAffine(large_image, M, large_image.shape)
        clip_half_length = 3*numpy.linalg.norm(axis1)
        i0 = int(round(rotated_image.shape[0]//2-clip_half_length))
        i1 = int(round(rotated_image.shape[0]//2+clip_half_length))
        j0 = int(round(rotated_image.shape[1]//2-clip_half_length))
        j1 = int(round(rotated_image.shape[1]//2+clip_half_length))
        clip_rotated_image = rotated_image[i0:(1+i1), j0:(1+j1)]
        vertical_sum = clip_rotated_image.sum(axis=0)
        horizontal_sum = clip_rotated_image.sum(axis=1)
        # print('vertical_sum', vertical_sum.max())
        # print('horizontal_sum', horizontal_sum.max())
        if vertical_sum.max() > horizontal_sum.max():
            log.debug('axis1 is y axis and axis2 is x axis')
            # axis1 is y axis and axis2 is x axis
            if markerdirection == 'L':
                axis = axis1
                axis1 = -axis2
                axis2 = axis
                coo = coordinate_system[:, 1, 0].copy()
                coordinate_system[:, 1, 0] = -coordinate_system[:, 1, 1].copy()
                coordinate_system[:, 1, 1] = coo
            elif markerdirection == 'L fliplr':
                axis = axis1
                axis1 = -axis2
                axis2 = -axis
                coo = coordinate_system[:, 1, 0].copy()
                coordinate_system[:, 1, 0] = -coordinate_system[:, 1, 1].copy()
                coordinate_system[:, 1, 1] = -coo
            elif markerdirection == 'L flipud':
                axis = axis1
                axis1 = axis2
                axis2 = axis
                coo = coordinate_system[:, 1, 0].copy()
                coordinate_system[:, 1, 0] = coordinate_system[:, 1, 1].copy()
                coordinate_system[:, 1, 1] = coo
            elif markerdirection == 'L flipud fliplr':
                axis = axis1
                axis1 = axis2
                axis2 = -axis
                coo = coordinate_system[:, 1, 0].copy()
                coordinate_system[:, 1, 0] = coordinate_system[:, 1, 1].copy()
                coordinate_system[:, 1, 1] = -coo
        else:
            log.debug('axis1 is x axis and axis2 is y axis')
            # axis1 is x axis and axis2 is y axis
            if markerdirection == 'L':
                # this can be reproduced by image '11.png' and
                # 90 degrees rotate first axis1
                axis2 = -axis2
                coordinate_system[:, 1, 1] = -coordinate_system[:, 1, 1]
            elif markerdirection == 'L fliplr':
                # this can be reproduced by image '12.png' and
                # 90 degrees rotate first axis1
                axis1 = -axis1
                axis2 = -axis2
                coordinate_system[:, 1, 0] = -coordinate_system[:, 1, 0]
                coordinate_system[:, 1, 1] = -coordinate_system[:, 1, 1]
            elif markerdirection == 'L flipud':
                # this can be reproduced by image '10.png' and
                # 90 degrees rotate first axis1
                pass
            elif markerdirection == 'L flipud fliplr':
                # this can be reproduced by image '08.png', '09.png' and
                # 90 degrees rotate first axis1
                axis1 = -axis1
                coordinate_system[:, 1, 0] = -coordinate_system[:, 1, 0]
    else:
        # no marker found
        log.error('ERROR: no marker found')
        return (None, 5, None, None)
    log.debug(f'final axis: |{axis1}| = {numpy.linalg.norm(axis1)}, '
              f'|{axis2}| = {numpy.linalg.norm(axis2)}')
    if draw_images[1]:
        cv2.imwrite(
            'ooo.png',
            array2image(draw_coordinate_system(
                image, zeropoint, axis1, axis2, coordinate_system)))
    # coordinate_system[:, 0, :] are the pixel coordinates
    # coordinate_system[:, 1, :] are the coordinates in an artificial system
    # filter blurry corners (3)
    size = 0.4 * (numpy.linalg.norm(axis1) + numpy.linalg.norm(axis2))
    coordinate_system = filter_blurry_corners(
        image, coordinate_system, size, min_sharpness)
    log.debug(f'keep {coordinate_system.shape[0]} good corners')
    if draw_images[2]:
        cv2.imwrite(
            'oooo.png',
            array2image(draw_coordinate_system(
                image, zeropoint, axis1, axis2, coordinate_system)))
    return coordinate_system, zeropoint, axis1, axis2
