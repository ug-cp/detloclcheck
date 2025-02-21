# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-02-06
:License: LGPL-3.0-or-later

aggregation of tests

You can run this file directly::

  env python3 checkerboard_image_class.py
  pytest-3 checkerboard_image_class.py

  env python3 checkerboard_image_class.py \
    TestCheckerboardImageClass.test_detect_localize_checkerboard_3

"""

import unittest


class TestCheckerboardImageClass(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2025-02-06

    env python3 checkerboard_image_class.py TestCheckerboardImageClass
    pytest-3 -k TestCheckerboardImageClass checkerboard_image_class.py
    """
    # pylint: disable=import-outside-toplevel

    def test_simpsons_rule(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-02-06
        """
        from detloclcheck.create_checkerboard_image.checkerboard_image_class \
            import simpsons_rule

        def f(x, y):
            # pylint: disable=unused-argument
            return 0
        result = simpsons_rule(f, 0, 1, 0, 1)
        self.assertAlmostEqual(result, 0.0)

        def f(x, y):
            # pylint: disable=unused-argument,function-redefined
            return 1
        result = simpsons_rule(f, 0, 1, 0, 1)
        self.assertAlmostEqual(result, 1.0)

        def f(x, y):
            # pylint: disable=unused-argument,function-redefined
            return 1
        result = simpsons_rule(f, 0, 10, 0, 5)
        self.assertAlmostEqual(result, 50.0)

        def f(x, y):
            # pylint: disable=function-redefined
            return y + 0.1 * x
        result = simpsons_rule(f, 0, 10, 0, 5)
        self.assertAlmostEqual(result, 150.0)

        def f(x, y):
            # pylint: disable=function-redefined
            return y + 0.1 * x + x * y
        result = simpsons_rule(f, 0, 10, 0, 5)
        self.assertAlmostEqual(result, 775.0)

    def test_nquad(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-02-06
        """
        from scipy.integrate import nquad

        def f(x, y):
            # pylint: disable=unused-argument
            return 1
        result, error = nquad(f, [[0, 1], [0, 1]])
        self.assertAlmostEqual(result, 1.0)
        self.assertLess(error, 1e-7)

        def f(x, y):
            # pylint: disable=unused-argument,function-redefined
            return 0
        result, error = nquad(f, [[0, 1], [0, 1]])
        self.assertAlmostEqual(result, 0.0)
        self.assertLess(error, 1e-7)

        def f(x, y):
            # pylint: disable=unused-argument,function-redefined
            return 1
        result, error = nquad(f, [[0, 10], [0, 5]])
        self.assertAlmostEqual(result, 50.0)
        self.assertLess(error, 1e-7)

        def f(x, y):
            # pylint: disable=function-redefined
            return y + 0.1 * x
        result, error = nquad(f, [[0, 10], [0, 5]])
        self.assertAlmostEqual(result, 150.0)
        self.assertLess(error, 1e-7)

        def f(x, y):
            # pylint: disable=function-redefined
            return y + 0.1 * x + x * y
        result, error = nquad(f, [[0, 10], [0, 5]])
        self.assertAlmostEqual(result, 775.0)
        self.assertLess(error, 1e-7)

    def test_simple_checkerboard(self):
        """
        :Author: Daniel Mohr
        :Date: 2025-02-06
        """
        import numpy
        from detloclcheck.create_checkerboard_image.checkerboard_image_class \
            import CheckerboardImageClass
        c = CheckerboardImageClass(3, (23, 23))
        n = 10
        img = numpy.zeros((n, n), dtype=numpy.uint8)
        for x in range(n):
            for y in range(n):
                img[x, y] = c(x, y)
        expected_result = numpy.array(
            [[255, 255, 128,   0,   0, 128, 255, 255, 128,   0],
             [255, 255, 128,   0,   0, 128, 255, 255, 128,   0],
             [128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
             [0,   0,   128, 255, 255, 128,   0,   0, 128, 255],
             [0,   0,   128, 255, 255, 128,   0,   0, 128, 255],
             [128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
             [255, 255, 128,   0,   0, 128, 255, 255, 128,   0],
             [255, 255, 128,   0,   0, 128, 255, 255, 128,   0],
             [128, 128, 128, 128, 128, 128, 128, 128, 128, 128],
             [0,   0,   128, 255, 255, 128,   0,   0, 128, 255]],
            dtype=numpy.uint8)
        numpy.testing.assert_array_equal(img, expected_result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
