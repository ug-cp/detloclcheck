.. DetLocLCheck documentation master file, created by
   sphinx-quickstart on Sun Jun 30 18:51:20 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DetLocLCheck's documentation
============================

``DetLocLCheck`` is a software tool designed for the Detection and
Localization of Checkerboard calibration targets containing L-shape
markers. This tool utilizes template matching for initial detection,
followed by refinement using OpenCV’s
`cornerSubPix <https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga354e0d7c86d0d9da75de9b9701a9a87e>`__
function to achieve subpixel accuracy. Finally, world coordinates are
assigned to the detected markers.

.. figure:: checkerboard_example_image.png
   :alt: Example image of a checkerboard calibration target containing L-shape marker

   Example image of a checkerboard calibration target containing L-shape marker

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   README.md
   script_detloclcheck
   module_detloclcheck
   test_coverage_report/index
   LICENSE.LESSER.md
   LICENSE.md

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
