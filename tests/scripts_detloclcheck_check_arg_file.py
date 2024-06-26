"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-06-26
:License: LGPL-3.0-or-later

aggregation of tests

You can run this file directly::

  env python3 scripts_detloclcheck_check_arg_file.py
  pytest-3 scripts_detloclcheck_check_arg_file.py

Or you can run only one test, e. g.::

  env python3 scripts_detloclcheck_check_arg_file.py TestCheck_arg_file
  pytest-3 -k TestCheck_arg_file scripts_detloclcheck_check_arg_file.py
"""

import unittest
import os
import argparse


class TestCheck_arg_file(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-26

    env python3 main.py TestImport
    pytest-3 -k TestImport main.py
    """

    def test_import(self):
        from detloclcheck.scripts.detloclcheck import check_arg_file
        with self.assertRaises(argparse.ArgumentTypeError):
            check_arg_file('foo')
        for filename in ['LICENSE.md', '../LICENSE.md']:
            if os.path.exists(filename):
                data = check_arg_file(filename)  # noqa: F841


if __name__ == '__main__':
    unittest.main(verbosity=2)
