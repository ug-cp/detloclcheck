"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-06-25
:License: LGPL-3.0-or-later

aggregation of tests

You can run this file directly::

  env python3 main.py
  pytest-3 main.py

Or you can run only one test, e. g.::

  env python3 main.py TestScriptsExecutable
  pytest-3 -k TestScriptsExecutable main.py
"""

import unittest
import subprocess


class TestScriptsExecutable(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-25

    env python3 main.py TestScriptsExecutable
    pytest-3 -k TestScriptsExecutable main.py
    """
    subprocess_timeout = 42

    def test_detloclcheck_executable_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-06-25

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_find_checkerboard_executable
        """
        cpi = subprocess.run(
            "detloclcheck",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=False)
        with self.assertRaises(subprocess.CalledProcessError):
            # parameter is necessary
            cpi.check_returncode()

    def test_detloclcheck_executable_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-06-25

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_find_checkerboard_executable
        """
        cpi = subprocess.run(
            "detloclcheck -h",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=True)
        # check at least minimal help output
        self.assertTrue(len(cpi.stdout) >= 42)
        # check begin of help output
        self.assertTrue(cpi.stdout.startswith(b'usage: detloclcheck'))
        # check end of help output
        self.assertTrue(cpi.stdout.strip().endswith(
            b'License: LGPL-3.0-or-later'))

    def test_detloclcheck_find_checkerboard_executable(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-06-25

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_find_checkerboard_executable
        """
        cpi = subprocess.run(
            "detloclcheck find_checkerboard -h",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=True)
        # check at least minimal help output
        self.assertTrue(len(cpi.stdout) >= 42)
        # check begin of help output
        self.assertTrue(cpi.stdout.startswith(
            b'usage: detloclcheck find_checkerboard'))
        # check end of help output
        self.assertTrue(cpi.stdout.strip().endswith(
            b'License: LGPL-3.0-or-later'))
