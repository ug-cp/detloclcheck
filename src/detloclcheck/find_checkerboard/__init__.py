# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:mod:`detloclcheck.find_checkerboard`
=====================================
   :synopsis: :mod:`detloclcheck` is a python module for Detection and
              Localization of a Checkerboard calibration target containing
              L-shape marker using template matching.

.. contents::

description
-----------

`DetLocLCheck` is a software tool for Detection and Localization of a
Checkerboard calibration target containing L-shape marker using
template matching.

functions
---------
.. currentmodule:: detloclcheck.find_checkerboard
.. autofunction:: find_checkerboard

submodules
----------
.. automodule:: detloclcheck.find_checkerboard.calculatetemplatematching
.. automodule:: detloclcheck.find_checkerboard.create_template
.. automodule:: detloclcheck.find_checkerboard.parallel_cornersubpix
.. automodule:: detloclcheck.find_checkerboard.set_black_border

copyright + license
-------------------
:Author: Daniel Mohr
:Date: 2025-01-29
:License: LGPL-3.0-or-later
:Copyright: (C) 2024, 2025 Daniel Mohr
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

from .find_checkerboard import find_checkerboard

__all__ = ["find_checkerboard"]
