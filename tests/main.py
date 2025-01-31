"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-10
:License: LGPL-3.0-or-later

aggregation of tests

You can run this file directly::

  env python3 main.py
  pytest-3 main.py

Or you can run only one test, e. g.::

  env python3 main.py TestScriptsExecutable
  pytest-3 -k TestScriptsExecutable main.py
"""

import subprocess
import tempfile
import unittest
import os

# pylint: disable=unused-import
try:
    from scripts_detloclcheck_check_arg_file \
        import TestCheckArgFile  # noqa: F401
    from detect_localize_checkerboard \
        import TestCheckDetectLocalizeCheckerboard  # noqa: F401
except ImportError:
    from tests.scripts_detloclcheck_check_arg_file \
        import TestCheckArgFile  # noqa: F401
    from tests.detect_localize_checkerboard \
        import TestCheckDetectLocalizeCheckerboard  # noqa: F401


class TestImport(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-10

    env python3 main.py TestImport
    pytest-3 -k TestImport main.py
    """

    def test_import(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-10
        """
        # pylint: disable=import-outside-toplevel
        import detloclcheck  # noqa: F401
        import detloclcheck.create_checkerboard_image  # noqa: F401
        import detloclcheck.create_coordinate_system  # noqa: F401
        import detloclcheck.find_checkerboard  # noqa: F401
        import detloclcheck.scripts  # noqa: F401
        import detloclcheck.tools  # noqa: F401


class TestScriptsExecutable(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-10

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

    def test_detloclcheck_create_checkerboard_executable(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-09

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_create_checkerboard_executable
        """
        cpi = subprocess.run(
            "detloclcheck create_checkerboard_image -h",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=True)
        # check at least minimal help output
        self.assertTrue(len(cpi.stdout) >= 42)
        # check begin of help output
        self.assertTrue(cpi.stdout.startswith(
            b'usage: detloclcheck create_checkerboard_image'))
        # check end of help output
        self.assertTrue(cpi.stdout.strip().endswith(
            b'License: LGPL-3.0-or-later'))

    def test_detloclcheck_create_checkerboard_0(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-23

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_create_checkerboard_0
        """
        filename = "foo.png"
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "foo.png")
            subprocess.run(
                "detloclcheck create_checkerboard_image "
                "-outfile " + filename + " -integrate_method 0",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            self.assertTrue(os.path.isfile(filename))

    def test_detloclcheck_create_checkerboard_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-23

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_create_checkerboard_1
        """
        filename = "foo.png"
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "bar.png")
            subprocess.run(
                "detloclcheck create_checkerboard_image "
                "-outfile " + filename + " -integrate_method 1",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            self.assertTrue(os.path.isfile(filename))

    def test_detloclcheck_create_checkerboard_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-23

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_create_checkerboard_2
        """
        filename = "foo.png"
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "baz.png")
            subprocess.run(
                "detloclcheck create_checkerboard_image "
                "-outfile " + filename + " -integrate_method 2",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=10*self.subprocess_timeout, check=True)
            self.assertTrue(os.path.isfile(filename))

    def test_detloclcheck_0(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-23

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_0
        """
        filename = "foo.png"
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "foo.png")
            subprocess.run(
                "detloclcheck create_checkerboard_image "
                "-outfile " + filename + " -integrate_method 0",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            self.assertTrue(os.path.isfile(filename))
            data_filename = \
                os.path.splitext(filename)[0] + '_ground_truth' + '.' + 'json'
            self.assertTrue(os.path.isfile(data_filename))
            subprocess.run(
                "detloclcheck find_checkerboard "
                "-f " + filename + " -crosssizes 11",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            data_filename = \
                os.path.splitext(filename)[0] + '.' + 'json'
            self.assertTrue(os.path.isfile(data_filename))

    def test_detloclcheck_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2024-07-23

        env python3 main.py \
        TestScriptsExecutable.test_detloclcheck_0
        """
        filename = "foo.png"
        with tempfile.TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "bar.png")
            subprocess.run(
                "detloclcheck create_checkerboard_image "
                "-outfile " + filename + " -integrate_method 0 "
                "-output_format mat",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            self.assertTrue(os.path.isfile(filename))
            data_filename = \
                os.path.splitext(filename)[0] + '_ground_truth' + '.' + 'mat'
            self.assertTrue(os.path.isfile(data_filename))
            subprocess.run(
                "detloclcheck find_checkerboard "
                "-f " + filename + " -crosssizes 11 -o mat",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            data_filename = \
                os.path.splitext(filename)[0] + '.' + 'mat'
            self.assertTrue(os.path.isfile(data_filename))


if __name__ == '__main__':
    unittest.main(verbosity=2)
