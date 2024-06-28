"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-06-28
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
import os
import sys


def run_find_checkerboard(args):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-28
    :License: LGPL-3.0-or-later
    """
    for filename in args.file:
        output_filename = \
            os.path.splitext(filename)[0] + '.' + args.output_format[0]
        pass


def check_arg_file(data):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-25
    :License: LGPL-3.0-or-later
    """
    if not os.path.isfile(data):
        msg = f'"{data}" is not a file'
        raise argparse.ArgumentTypeError(msg)
    return data


def check_arg_crosssizes(data):
    """
    :Author: Daniel Mohr
    :Date: 2024-06-25
    :License: LGPL-3.0-or-later
    """
    try:
        data = int(data)
    except ValueError:
        msg = f'"{data}" can not be interpreted as int'
        raise argparse.ArgumentTypeError(msg)
    if data % 2 == 0:
        msg = f'"{data}" is not odd'
        raise argparse.ArgumentTypeError(msg)
    return data


def main():
    """
    :Author: Daniel Mohr
    :Date: 2024-06-28
    :License: LGPL-3.0-or-later
    """
    epilog = "Author: Daniel Mohr\n"
    epilog += "Date: 2024-06-25\n"
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
        help='Set the file(s) to use. ',
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
        '-max_distance_factor_range',
        nargs="+",
        type=float,
        required=False,
        default=(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.),
        dest='max_distance_factor_range',
        help='Set the possible maximal distance factors. Typically it is '
        'assumed that the x size and y size of a checkerboard cell is equal. '
        'But if the checkerboard is rotated against the focus plane then other '
        'x/y are possible. This list defines which factors are maximal '
        'allowed. We try first to find the coordinate axis with the maximal '
        'the first factor. If this is not possible, we take the next and so '
        'on. default: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.',
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
    args = parser.parse_args()
    if args.subparser_name is not None:
        sys.exit(args.func(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
