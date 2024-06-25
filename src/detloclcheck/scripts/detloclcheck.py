"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2024-06-25
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


def main():
    """
    :Author: Daniel Mohr
    :Date: 2024-06-25
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
    parser.add_argument(
        '-file',
        nargs="+",
        type=check_arg_file,
        required=True,
        dest='file',
        help='Set the file(s) to use. ',
        metavar='f')
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
    args = parser.parse_args()
    if args.subparser_name is not None:
        sys.exit(args.func(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
