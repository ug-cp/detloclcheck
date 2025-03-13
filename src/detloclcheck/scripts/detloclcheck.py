# SPDX-FileCopyrightText: 2024-2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
:Author: Daniel Mohr
:Email: daniel.mohr@uni-greifswald.de
:Date: 2025-03-10
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
import importlib.metadata
import json
import logging
import logging.handlers
import os
import sys

import cv2
import numpy
import scipy.io

from detloclcheck.create_checkerboard_image import create_checkerboard_image
from detloclcheck.detect_localize_checkerboard import \
    detect_localize_checkerboard


def run_find_checkerboard(args):
    """
    :Author: Daniel Mohr
    :Date: 2025-02-24
    :License: LGPL-3.0-or-later
    """
    errorcode = 0
    log = logging.getLogger('detloclcheck.run_find_checkerboard')
    for filename in args.file:
        log.info('handle file "%s"', filename)
        image = cv2.imread(filename)
        if image is None:
            log.error('file "%s" cannot be read as image', filename)
            return 1
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        coordinate_system, zeropoint, axis1, axis2 = \
            detect_localize_checkerboard(
                gray_image, args.crosssizes, args.angles,
                hit_bound=args.hit_bound[0],
                min_sharpness=args.min_sharpness,
                run_parallel=args.run_parallel,
                max_distance_factor_range=args.max_distance_factor_range,
                log=None)
        if coordinate_system is None:
            log.error(
                'ERROR %i during handling file "%s"', zeropoint, filename)
            errorcode += zeropoint
            continue
        for output_format in args.output_format:
            output_filename = \
                os.path.splitext(filename)[0] + '.' + output_format
            if output_format == 'json':
                with open(output_filename, 'w', encoding='utf8') as fd:
                    json.dump(
                        {'coordinate_system': coordinate_system.tolist(),
                         'zeropoint': zeropoint.tolist(),
                         'axis1': axis1.tolist(), 'axis2': axis2.tolist()},
                        fd, indent=args.json_indent[0])
            if output_format == 'mat':
                scipy.io.savemat(
                    output_filename,
                    {'coordinate_system': coordinate_system,
                     'zeropoint': zeropoint,
                     'axis1': axis1, 'axis2': axis2})
            log.info('wrote result with %i good corners to "%s"',
                     coordinate_system.shape[0],
                     output_filename)
    return errorcode


def run_create_checkerboard_image(args):
    """
    :Author: Daniel Mohr
    :Date: 2025-02-24
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck.run_create_checkerboard_image')
    zeropoint, coordinates, image = create_checkerboard_image(
        args.m[0], args.n[0], args.size[0],
        zeropoint=args.zeropoint, integrate_method=args.integrate_method[0],
        transition_value=args.transition_value[0], scale=args.scale[0])
    cv2.imwrite(args.outfile[0], image)
    for output_format in args.output_format:
        output_filename = \
            os.path.splitext(args.outfile[0])[0] + '_ground_truth' \
            + '.' + output_format
        if output_format == 'json':
            with open(output_filename, 'w', encoding='utf8') as fd:
                json.dump(
                    {'coordinates': coordinates.tolist(),
                     'zeropoint': zeropoint},
                    fd, indent=args.json_indent[0])
        if args.output_format[0] == 'mat':
            scipy.io.savemat(
                output_filename,
                {'coordinates': coordinates,
                 'zeropoint': zeropoint})
        log.info('wrote result to "%s"', output_filename)
    return 0


def run_visualize(args):
    """
    :Author: Daniel Mohr
    :Date: 2025-03-10
    :License: LGPL-3.0-or-later
    """
    # pylint: disable=import-outside-toplevel
    import matplotlib.pyplot
    log = logging.getLogger('detloclcheck.run_visualize')
    if args.dosubplot:
        ncolumns = int(numpy.sqrt(len(args.data_file_name)))
        nrows = int(numpy.ceil(len(args.data_file_name) / ncolumns))
        assert ncolumns * nrows >= len(args.data_file_name)
    for fid, data_file_name in enumerate(args.data_file_name):
        if args.dosubplot:
            matplotlib.pyplot.subplot(
                nrows, ncolumns, 1 + fid)
        visualize_image = False
        if ((args.image_file_name is not None) and
                (fid < len(args.image_file_name))):
            visualize_image = True
            log.debug('visualize "%s" with with"%s"',
                      data_file_name, args.image_file_name[fid])
        else:
            log.debug('visualize "%s"', data_file_name)
        _, file_extension = os.path.splitext(data_file_name)
        if file_extension.lower() == '.json':
            with open(data_file_name, 'r', encoding='utf8') as fd:
                data = json.load(fd)
                coordinate_system = numpy.array(data['coordinate_system'])
                zeropoint = numpy.array(data['zeropoint'])
        elif file_extension.lower() == '.mat':
            data = scipy.io.loadmat(data_file_name)
            coordinate_system = data['coordinate_system']
            zeropoint = numpy.reshape(data['zeropoint'], (2,))
        else:
            log.error('ERROR: do not understand file extension "%s"',
                      file_extension)
            return 1
        log.debug('axis1: %s', data['axis1'])
        log.debug('axis2: %s', data['axis2'])
        if visualize_image:
            gray_image = cv2.imread(
                args.image_file_name[fid], cv2.COLOR_BGR2GRAY)
            matplotlib.pyplot.imshow(gray_image, cmap="gray")
        matplotlib.pyplot.plot(
            coordinate_system[:, 0, 0],
            coordinate_system[:, 0, 1],
            'r2', markersize=20)
        matplotlib.pyplot.plot(
            zeropoint[0], zeropoint[1],
            'b1', markersize=20)
        for i in range(coordinate_system.shape[0]):
            matplotlib.pyplot.text(
                coordinate_system[i, 0, 0], coordinate_system[i, 0, 1],
                f'({int(coordinate_system[i, 1, 0])},'
                f'{int(coordinate_system[i, 1, 1])})',
                color='g', fontsize='small', rotation=45)
        if not args.dosubplot:
            matplotlib.pyplot.show()
    if args.dosubplot:
        matplotlib.pyplot.show()
    return 0


def run_version(_):
    """
    :Author: Daniel Mohr
    :Date: 2025-02-25
    :License: LGPL-3.0-or-later
    """
    version = importlib.metadata.version(__package__.split(".", maxsplit=1)[0])
    print(f'DetLocLCheck version {version}')
    return 0


def check_arg_file(data):
    """
    :Author: Daniel Mohr
    :Date: 2024-07-01
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck.check_arg_file')
    log.debug('handle file "%s"', data)
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
    log.debug('check crosssize "%s"', data)
    try:
        data = int(data)
    except ValueError:
        msg = f'"{data}" can not be interpreted as int'
        # pylint: disable=raise-missing-from
        raise argparse.ArgumentTypeError(msg)
    if data % 2 == 0:
        msg = f'"{data}" is not odd'
        raise argparse.ArgumentTypeError(msg)
    return data


def my_argument_parser():
    """
    :Author: Daniel Mohr
    :Date: 2025-03-10
    :License: LGPL-3.0-or-later
    """
    epilog = "Example:\n\n"
    epilog += "detloclcheck create_checkerboard_image -outfile foo.png\n"
    epilog += "detloclcheck find_checkerboard -f foo.png\n"
    epilog += "detloclcheck visualize foo.json -i foo.png\n\n"
    epilog += "Author: Daniel Mohr\n"
    epilog += "Date: 2025-03-10\n"
    epilog += "DetLocLCheck Version: "
    epilog += importlib.metadata.version(
        __package__.split('.', maxsplit=1)[0]) + "\n"
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
        'containing L-shape marker using template matching.',
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
        nargs='+',
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
        '-json_indent',
        nargs=1,
        type=int,
        required=False,
        default=[None],
        dest='json_indent',
        help='Set the indent in the json output. On default a minimal file '
        'size is achieved. Setting any numbers will lead to a better human '
        'readable output with a larger file size. '
        'default: None',
        metavar='f')
    parser_find_checkerboard.add_argument(
        '-crosssizes',
        nargs="+",
        type=check_arg_crosssizes,
        required=False,
        default=(11, 23),
        dest='crosssizes',
        help='Set a list of cross sizes to test. You can use odd integers. '
        'This is used during template matching. default: 11, 23',
        metavar='s')
    parser_find_checkerboard.add_argument(
        '-angles',
        nargs="+",
        type=check_arg_crosssizes,
        required=False,
        default=(0.0,  22.5,  45.0,  67.5,  90.0, 112.5, 135.0, 157.5),
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
    # subparser create_checkerboard_image
    parser_create_checkerboard_image = subparsers.add_parser(
        'create_checkerboard_image',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: detloclcheck create_checkerboard_image -h',
        description='detloclcheck create_checkerboard_image is a python script'
        ' to create an artificial image of a checkerboard.',
        epilog=epilog)
    parser_create_checkerboard_image.set_defaults(
        func=run_create_checkerboard_image)
    parser_create_checkerboard_image.add_argument(
        '-outfile',
        nargs=1,
        type=str,
        required=True,
        dest='outfile',
        help='Set the filename to write result image. '
        'The coordinates will be written to a file with a different postfix.',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-output_format',
        nargs='+',
        type=str,
        choices=['json', 'mat'],
        required=False,
        default=['json'],
        dest='output_format',
        help='Set the output format to use for the coordinates. '
        '"json" will save the result as a json file. '
        '"mat" will save the result as a MATLAB-style .mat file. '
        'default: json',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-json_indent',
        nargs=1,
        type=int,
        required=False,
        default=[None],
        dest='json_indent',
        help='Set the indent in the json output. On default a minimal file '
        'size is achieved. Setting any numbers will lead to a better human '
        'readable output with a larger file size. '
        'default: None',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-size',
        nargs=1,
        type=float,
        required=False,
        default=[15.0],
        dest='size',
        help='size of a checkerboard field. default: 15.0',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-scale',
        nargs=1,
        type=float,
        required=False,
        default=[1.0],
        dest='scale',
        help='scaling factor. default 1.0',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-m',
        nargs=1,
        type=int,
        required=False,
        default=[8],
        dest='m',
        help='number rows of checkerboard fields. default: 8',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-n',
        nargs=1,
        type=int,
        required=False,
        default=[8],
        dest='n',
        help='number columns of checkerboard fields. default: 8',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-zeropoint',
        nargs=2,
        type=float,
        required=False,
        default=None,
        dest='zeropoint',
        help='zeropoint in opencv coordinate. default: [middle of the image]',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-integrate_method',
        nargs=1,
        type=int,
        choices=[0, 1, 2],
        required=False,
        default=[0],
        dest='integrate_method',
        help='Set the method used for integration over one pixel. '
        '0: no integration. 1: simple Simpson\'s Rule. '
        '2: use of scipy.integrate.nquad. '
        'default: 0',
        metavar='f')
    parser_create_checkerboard_image.add_argument(
        '-transition_value',
        nargs=1,
        type=int,
        choices=range(256),
        required=False,
        default=[128],
        dest='transition_value',
        help='Set the transition value between white and black areas. '
        'For a value of 255 the light areas in the image run out. '
        'For a value of 0 the reverse effect is simulated. '
        'default: 128',
        metavar='f')
    parser_visualize = subparsers.add_parser(
        'visualize',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: detloclcheck visualize -h',
        description='detloclcheck visualize is a python script'
        ' to visualize the data found by detloclcheck find_checkerboard.',
        epilog=epilog)
    parser_visualize.set_defaults(
        func=run_visualize)
    parser_visualize.add_argument(
        dest='data_file_name',
        nargs='+',
        type=str,
        metavar='data',
        help='Name of the data file(s) to visualize. '
        'This could be the of detloclcheck find_checkerboard and a '
        'json or a mat file.')
    parser_visualize.add_argument(
        '-image_file_name',
        nargs='+',
        type=str,
        required=False,
        dest='image_file_name',
        metavar='img',
        help='Name of the image file(s) to visualize.')
    parser_visualize.add_argument(
        '-subplot',
        default=False,
        required=False,
        action='store_true',
        dest='dosubplot',
        help='If set this flag, will plot in subplots.')
    parser_version = subparsers.add_parser(
        'version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='return version of detloclcheck',
        description='display version information of detloclcheck',
        epilog=epilog)
    parser_version.set_defaults(
        func=run_version)
    return parser


def main():
    """
    :Author: Daniel Mohr
    :Date: 2025-02-24
    :License: LGPL-3.0-or-later
    """
    log = logging.getLogger('detloclcheck')
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(name)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S %Z'))
    log.addHandler(stdout_handler)
    log.setLevel(logging.DEBUG)
    parser = my_argument_parser()
    args = parser.parse_args()
    file_handler = None
    if hasattr(args, 'log_file') and (args.log_file is not None):
        file_handler = logging.handlers.WatchedFileHandler(args.log_file[0])
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S_%Z'))
        log.addHandler(file_handler)
        log.debug('added logging to file "%s"', args.log_file[0])
    if args.subparser_name is not None:
        if args.subparser_name != 'version':
            log.info('start detloclcheck %s',
                     importlib.metadata.version(
                         __package__.split('.', maxsplit=1)[0]))
            log.info("started as/with: %s", " ".join(sys.argv))
        exit_status = args.func(args)
    else:
        parser.print_help()
        exit_status = 1
    if file_handler is not None:
        file_handler.flush()
    stdout_handler.flush()
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
