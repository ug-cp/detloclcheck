# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-01-31
:License: LGPL-3.0-or-later

aggregation of tests

You can run this file directly::

  env python3 detect_localize_checkerboard.py
  pytest-3 detect_localize_checkerboard.py

  env python3 detect_localize_checkerboard.py \
    TestCheck_detect_localize_checkerboard.test_detect_localize_checkerboard_3

"""

import unittest

import numpy


def calculate_square_distances(x0, y0, x1, y1):
    xd = ((numpy.ones((x1.shape[0], 1)) * x0) -
          (numpy.ones((x0.shape[0], 1)) * x1).transpose())
    yd = ((numpy.ones((y1.shape[0], 1)) * y0) -
          (numpy.ones((y0.shape[0], 1)) * y1).transpose())
    return numpy.square(xd) + numpy.square(yd)


def coordinates_root_mean_square_error(coordinates, coordinate_system):
    dist = calculate_square_distances(
        coordinates[:, 0], coordinates[:, 1],
        coordinate_system[:, 0, 0], coordinate_system[:, 0, 1])
    square_distance_sum = 0.0
    for i in range(coordinates.shape[0]):
        index = numpy.unravel_index(dist.argmin(), dist.shape)
        square_distance_sum += dist[index]
        dist[:, index[1]] = numpy.inf
        dist[index[0], :] = numpy.inf
        root_mean_square_error = \
            numpy.sqrt(square_distance_sum /
                       coordinates.shape[0])
    return root_mean_square_error


class TestCheck_detect_localize_checkerboard(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2025-01-31

    env python3 detect_localize_checkerboard.py \
        TestCheck_detect_localize_checkerboard
    pytest-3 -k TestCheck_detect_localize_checkerboard \
        detect_localize_checkerboard.py
    """

    def test_detect_localize_checkerboard_0a(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-01-30
        """
        from detloclcheck.create_checkerboard_image import \
            create_checkerboard_image
        from detloclcheck.detect_localize_checkerboard import \
            detect_localize_checkerboard
        ground_truth_zeropoint, coordinates, image = \
            create_checkerboard_image(8, 8, 15)
        coordinate_system, zeropoint, axis1, axis2 = \
            detect_localize_checkerboard(
                image, crosssizes=(11,),
                angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))
        numpy.testing.assert_almost_equal(
            ground_truth_zeropoint, zeropoint, decimal=3)
        root_mean_square_error = coordinates_root_mean_square_error(
            coordinates, coordinate_system)
        self.assertLess(root_mean_square_error, 0.02)

    def test_detect_localize_checkerboard_0b(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-01-31
        """
        from detloclcheck.create_checkerboard_image import \
            create_checkerboard_image
        from detloclcheck.detect_localize_checkerboard import \
            detect_localize_checkerboard
        angles = (0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5)
        # a smaller movement is not detectable in the image (identical images)
        for (setzeropoint, maxdelta) in (([59.0, 59.0], (0.00007, 0.2)),
                                         ([59.0, 59.5], (0.0001, 0.2)),
                                         ([59.2, 59.0], (0.4, 0.4)),
                                         ([59.7, 59.0], (0.2, 0.3))):
            ground_truth_zeropoint, coordinates, image = \
                create_checkerboard_image(
                    8, 8, 15, zeropoint=setzeropoint, integrate_method=0)
            coordinate_system, zeropoint, axis1, axis2 = \
                detect_localize_checkerboard(
                    image, crosssizes=(11,),
                    angles=angles)
            zeropoint_error = numpy.linalg.norm(
                ground_truth_zeropoint-zeropoint)
            root_mean_square_error = coordinates_root_mean_square_error(
                coordinates, coordinate_system)
            print(setzeropoint, zeropoint_error, root_mean_square_error)
            self.assertLess(zeropoint_error, maxdelta[0])
            self.assertLess(root_mean_square_error, maxdelta[1])

    def test_detect_localize_checkerboard_1a(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-01-30
        """
        from detloclcheck.create_checkerboard_image import \
            create_checkerboard_image
        from detloclcheck.detect_localize_checkerboard import \
            detect_localize_checkerboard
        ground_truth_zeropoint, coordinates, image = create_checkerboard_image(
            8, 8, 15, integrate_method=1)
        coordinate_system, zeropoint, axis1, axis2 = \
            detect_localize_checkerboard(
                image, crosssizes=(11,),
                angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))
        numpy.testing.assert_almost_equal(
            ground_truth_zeropoint, zeropoint, decimal=3)
        root_mean_square_error = coordinates_root_mean_square_error(
            coordinates, coordinate_system)
        self.assertLess(root_mean_square_error, 0.002)

    def test_detect_localize_checkerboard_1b(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-01-31
        """
        from detloclcheck.create_checkerboard_image import \
            create_checkerboard_image
        from detloclcheck.detect_localize_checkerboard import \
            detect_localize_checkerboard
        angles = (0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5)
        # a smaller movement is not detectable in the image (identical images)
        for (setzeropoint, maxdelta) in (([59.0, 59.0], (0.00007, 0.09)),
                                         ([59.0, 59.2], (0.2, 0.3)),
                                         ([59.0, 59.5], (0.0002, 0.07)),
                                         ([59.0, 59.7], (0.2, 0.3)),
                                         ([59.2, 59.0], (0.2, 0.3)),
                                         ([59.3, 59.3], (0.2, 0.2)),
                                         ([59.2, 59.5], (0.2, 0.2)),
                                         ([59.3, 59.7], (0.2, 0.2)),
                                         ([59.5, 59.0], (0.0002, 0.07)),
                                         ([59.5, 59.2], (0.2, 0.2)),
                                         ([59.5, 59.5], (0.00005, 0.002)),
                                         ([59.5, 59.7], (0.1, 0.1)),
                                         ([59.8, 59.0], (0.2, 0.3)),
                                         ([59.8, 59.0], (0.2, 0.3)),
                                         ([59.7, 59.5], (0.1, 0.2)),
                                         ([59.7, 59.8], (0.3, 0.3)),
                                         ([59.5, 60.0], (0.0002, 0.07)),
                                         ([59.5, 60.1], (0.3, 0.3)),
                                         ([59.5, 60.5], (0.00005, 0.002))):
            ground_truth_zeropoint, coordinates, image = \
                create_checkerboard_image(
                    8, 8, 15, zeropoint=setzeropoint, integrate_method=1)
            coordinate_system, zeropoint, axis1, axis2 = \
                detect_localize_checkerboard(
                    image, crosssizes=(11,),
                    angles=angles)
            zeropoint_error = numpy.linalg.norm(
                ground_truth_zeropoint-zeropoint)
            root_mean_square_error = coordinates_root_mean_square_error(
                coordinates, coordinate_system)
            self.assertLess(zeropoint_error, maxdelta[0])
            self.assertLess(root_mean_square_error, maxdelta[1])

    def test_detect_localize_checkerboard_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-01-30
        """
        from detloclcheck.create_checkerboard_image import \
            create_checkerboard_image
        from detloclcheck.detect_localize_checkerboard import \
            detect_localize_checkerboard
        ground_truth_zeropoint, coordinates, image = create_checkerboard_image(
            8, 8, 15, integrate_method=2)
        coordinate_system, zeropoint, axis1, axis2 = \
            detect_localize_checkerboard(
                image, crosssizes=(11,),
                angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))
        numpy.testing.assert_almost_equal(
            ground_truth_zeropoint, zeropoint, decimal=3)
        root_mean_square_error = coordinates_root_mean_square_error(
            coordinates, coordinate_system)
        self.assertLess(root_mean_square_error, 0.02)


if __name__ == '__main__':
    unittest.main(verbosity=2)
