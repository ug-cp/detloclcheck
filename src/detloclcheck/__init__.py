# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:mod:`detloclcheck`
===================
   :synopsis: :mod:`detloclcheck` is a python module for Detection and
              Localization of a Checkerboard calibration target containing
              L shape marker using template matching.

.. contents::

description
===========

`DetLocLCheck` is a software tool for Detection and Localization of a
Checkerboard calibration target containing L shape marker using
template matching.

submodules
==========
.. automodule:: detloclcheck.create_checkerboard_image
.. automodule:: detloclcheck.create_coordinate_system
.. automodule:: detloclcheck.detect_localize_checkerboard
.. automodule:: detloclcheck.find_checkerboard
.. automodule:: detloclcheck.tools
.. automodule:: detloclcheck.scripts

copyright + license
===================
:Author: Daniel Mohr
:Date: 2025-02-20
:License: LGPL-3.0-or-later
:Copyright: (C) 2024-2025 Daniel Mohr
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

import importlib.metadata

__version__ = importlib.metadata.version(__package__)
