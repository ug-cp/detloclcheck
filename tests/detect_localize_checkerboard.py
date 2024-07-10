"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-10
:License: LGPL-3.0-or-later

aggregation of tests

You can run this file directly::

  env python3 detect_localize_checkerboard.py
  pytest-3 detect_localize_checkerboard.py
"""

import unittest


class TestCheck_detect_localize_checkerboard(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-26

    env python3 detect_localize_checkerboard.py \
        TestCheck_detect_localize_checkerboard
    pytest-3 -k TestCheck_detect_localize_checkerboard \
        detect_localize_checkerboard.py
    """

    def test_detect_localize_checkerboard_0(self):
        from detloclcheck.create_checkerboard_image \
            import create_checkerboard_image
        from detloclcheck.detect_localize_checkerboard \
            import detect_localize_checkerboard
        image = create_checkerboard_image(8, 8, 15)
        coordinate_system, zeropoint, axis1, axis2 = \
            detect_localize_checkerboard(
                image, crosssizes=(11,),
                angles=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5))
        print('zeropoint', zeropoint)


if __name__ == '__main__':
    unittest.main(verbosity=2)
