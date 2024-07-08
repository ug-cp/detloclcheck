"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-07-08
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

import argparse
import logging
import logging.handlers
import os
import sys

import cv2

from detloclcheck.find_checkerboard import find_checkerboard
from detloclcheck.tools import filter_blurry_corners
from detloclcheck.create_coordinate_system import create_coordinate_system


def run_find_checkerboard(args):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-08
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck.run_find_checkerboard')
    for filename in args.file:
        log.info(f'handle file "{filename}"')
        # output_filename = \
        #     os.path.splitext(filename)[0] + '.' + args.output_format[0]
        image = cv2.imread(filename)
        if image is None:
            log.error(f'file "{filename}" cannot be read as image')
            return 1
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        coordinates = find_checkerboard(
            gray_image,
            crosssizes=args.crosssizes,
            angles=args.angles,
            hit_bound=args.hit_bound[0],
            min_sharpness=args.min_sharpness[0],
            run_parallel=args.run_parallel)
        if coordinates is None:
            log.error('ERROR: no inner corners detected')
            return 1
        # filter blurry corners (2)
        coordinates = filter_blurry_corners(
            gray_image, coordinates, args.crosssizes[0], args.min_sharpness[1])
    if coordinates.shape[0] < 24:
        log.error(
            'ERROR: only %i corners detected, '
            'but we need at least 24 for marker detection',
            coordinates.shape[0])
        return 1
    log.debug(f'go on with {coordinates.shape[0]} corners')
    coordinate_system, zeropoint, axis1, axis2 = create_coordinate_system(
        gray_image, coordinates, args.max_distance_factor_range,
        min_sharpness=args.min_sharpness[2])
    if coordinate_system is None:
        return zeropoint  # zeropoint is used as error code
    return 0


def check_arg_file(data):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck.check_arg_file')
    log.debug(f'handle file "{data}"')
    if not os.path.isfile(data):
        msg = f'"{data}" is not a file'
        raise argparse.ArgumentTypeError(msg)
    return data


def check_arg_crosssizes(data):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck.check_arg_crosssizes')
    log.debug(f'check crosssize "{data}"')
    try:
        data = int(data)
    except ValueError:
        msg = f'"{data}" can not be interpreted as int'
        raise argparse.ArgumentTypeError(msg)
    if data % 2 == 0:
        msg = f'"{data}" is not odd'
        raise argparse.ArgumentTypeError(msg)
    return data


def my_argument_parser():
    epilog = "Author: Daniel Mohr\n"
    epilog += "Date: 2024-07-01\n"
    epilog += "License: LGPL-3.0-or-later"
    epilog += "\n\n"
    parser = argparse.ArgumentParser(
        description='detloclcheck is a python script.',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # subparsers
    subparsers = parser.add_subparsers(
        dest='subparser_name',
        help='There are different sub-commands with there own flags.')
    # subparser find_checkerboard
    parser_find_checkerboard = subparsers.add_parser(
        'find_checkerboard',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: detloclcheck find_checkerboard -h',
        description='detloclcheck find_checkerboard is a python script for '
        'detection and localization of a checkerboard calibration target '
        'containing L shape marker using template matching.',
        epilog=epilog)
    parser_find_checkerboard.set_defaults(func=run_find_checkerboard)
    parser_find_checkerboard.add_argument(
        '-file',
        nargs="+",
        type=check_arg_file,
        required=True,
        dest='file',
        help='Set the file(s) to use.',
        metavar='f')
    parser_find_checkerboard.add_argument(
        '-output_format',
        nargs=1,
        type=str,
        choices=['json', 'mat'],
        required=False,
        default=['json'],
        dest='output_format',
        help='Set the output format to use. '
        '"json" will save the result as a json file. '
        '"mat" will save the result as a MATLAB-style .mat file. '
        'default: json',
        metavar='f')
    parser_find_checkerboard.add_argument(
        '-crosssizes',
        nargs="+",
        type=check_arg_crosssizes,
        required=False,
        default=[15, 23],
        dest='crosssizes',
        help='Set a list of cross sizes to test. You can use odd integers. '
        'This is used during template matching. default: 15, 23',
        metavar='s')
    parser_find_checkerboard.add_argument(
        '-angles',
        nargs="+",
        type=check_arg_crosssizes,
        required=False,
        default=[0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5],
        dest='angles',
        help='Set a list of angles to test. '
        'This is used during template matching. '
        'default: 0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5',
        metavar='a')
    parser_find_checkerboard.add_argument(
        '-hit_bound',
        nargs=1,
        type=float,
        required=False,
        default=[0.93],
        dest='hit_bound',
        help='This value is used during template matching. A checkerboard '
        'corner has to reach at least this value. default: 0.93',
        metavar='x')
    parser_find_checkerboard.add_argument(
        '-min_sharpness',
        nargs=3,
        type=float,
        required=False,
        default=(100, 500, 1000),
        dest='min_sharpness',
        help='At 3 steps blurry corners are removed. These list of values '
        'define the minimal sharpness for a good corner and others are '
        'intepreted as blurry. default: 100, 500, 1000',
        metavar='x')
    parser_find_checkerboard.add_argument(
        '-max_distance_factor_range',
        nargs="+",
        type=float,
        required=False,
        default=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.),
        dest='max_distance_factor_range',
        help='Set the possible maximal distance factors. Typically it is '
        'assumed that the x size and y size of a checkerboard cell is equal. '
        'But if the checkerboard is rotated against the focus plane then '
        'other x/y are possible. This list defines which factors are maximal '
        'allowed. We try first to find the coordinate axis with the maximal '
        'the first factor. If this is not possible, we take the next and so '
        'on. default: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.',
        metavar='x')
    parser_find_checkerboard.add_argument(
        '-log_file',
        nargs=1,
        type=str,
        required=False,
        dest='log_file',
        help='Set the log file. If not given logging is only done on stdout.',
        metavar='f')
    parser_find_checkerboard.add_argument(
        '-run_parallel',
        default=False,
        required=False,
        action='store_true',
        dest='run_parallel',
        help='If set this flag, will try to do things in parallel.')
    return parser


def main():
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck')
    ch = logging.StreamHandler()
    ch.setFormatter(
        logging.Formatter(
            '%(asctime)s %(name)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S %Z'))
    log.addHandler(ch)
    log.setLevel(logging.DEBUG)
    parser = my_argument_parser()
    args = parser.parse_args()
    if hasattr(args, 'log_file') and (args.log_file is not None):
        fh = logging.handlers.WatchedFileHandler(args.log_file[0])
        fh.setFormatter(
            logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S_%Z'))
        log.addHandler(fh)
        log.debug(f'added logging to file "{args.log_file[0]}"')
    if args.subparser_name is not None:
        log.info('start detloclcheck')
        sys.exit(args.func(args))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
