function load_detloclcheck(varargin)
%load_detloclcheck loads data, which were be created with
%'detloclcheck find_checkerboard' and adapt it to the
% octave and matlab index system.
%
%load_detloclcheck(filename)
%load_detloclcheck filename
%loads all variables 'axis1', 'axis2', 'coordinate_system' and 'zeropoint'
%from the file with the name filename.
%
%load_detloclcheck(filename, var1, var2, ...)
%load_detloclcheck filename var1 var2 ...
%loads only some variables var1, var2, ... from the file with the name
%filename.
%
%The data will be put in the caller workspace as the variables:
%  'axis1', 'axis2', 'coordinate_system', 'zeropoint'
%
%Example 1:
%
%  load_detloclcheck('foo.mat')
%  img = imread("foo.png");
%  imshow(img)
%  hold on
%  plot(coordinate_system(:, 1, 1), coordinate_system(:, 1, 2), ...
%      'rx', 'MarkerSize', 30, 'LineWidth', 3)
%  plot(zeropoint(1), zeropoint(2), ...
%      'b+', 'MarkerSize', 30, 'LineWidth', 3)
%  hold off
%
%Example 2:
%
%  load_detloclcheck 'foo.mat' 'zeropoint'
%  img = imread("foo.png");
%  imshow(img)
%  hold on
%  plot(zeropoint(1), zeropoint(2), ...
%      'b+', 'MarkerSize', 30, 'LineWidth', 3)
%  hold off
%
% Author: Daniel Mohr
% Date: 2025-01-30
% License: LGPL-3.0-or-later
% SPDX-FileCopyrightText: 2025 Daniel Mohr <daniel.mohr@uni-greifswald.de>
% SPDX-License-Identifier: LGPL-3.0-or-later

parser = inputParser;
validfilename = @(x) isfile(x);
addRequired(parser, 'filename', validfilename);
validopt = @(x) ischar(x);
addOptional(parser, 'opt1', '', validopt);
addOptional(parser, 'opt2', '', validopt);
addOptional(parser, 'opt3', '', validopt);
addOptional(parser, 'opt4', '', validopt);
parse(parser, varargin{:});
if ismember('opt1', parser.UsingDefaults)
  load(parser.Results.filename, ...
       'axis1', 'axis2', 'coordinate_system', 'zeropoint');
else
  if ismember('opt2', parser.UsingDefaults)
    load(parser.Results.filename, parser.Results.opt1)
  else
    if ismember('opt3', parser.UsingDefaults)
      load(parser.Results.filename, parser.Results.opt1, parser.Results.opt2)
    else
      if ismember('opt4', parser.UsingDefaults)
	load(parser.Results.filename, parser.Results.opt1, parser.Results.opt2, parser.Results.opt3)
      else
	load(parser.Results.filename, parser.Results.opt1, parser.Results.opt2, parser.Results.opt3, parser.Results.opt4)
      end
    end
  end
end

if ismember('opt1',parser.UsingDefaults) || (strcmp(parser.Results.opt1, 'coordinate_system') || strcmp(parser.Results.opt2, 'coordinate_system') || strcmp(parser.Results.opt3, 'coordinate_system') || strcmp(parser.Results.opt4, 'coordinate_system'))
  % adapt to matlab index system
  coordinate_system(:, 1, :) = 1 + coordinate_system(:, 1, :);
  assignin('caller', 'coordinate_system', coordinate_system)
end
if ismember('opt1',parser.UsingDefaults) || (strcmp(parser.Results.opt1, 'zeropoint') || strcmp(parser.Results.opt2, 'zeropoint') || strcmp(parser.Results.opt3, 'zeropoint') || strcmp(parser.Results.opt4, 'zeropoint'))
  % adapt to matlab index system
  assignin('caller', 'zeropoint', 1 + zeropoint);
end
if ismember('opt1',parser.UsingDefaults) || (strcmp(parser.Results.opt1, 'axis1') || strcmp(parser.Results.opt2, 'axis1') || strcmp(parser.Results.opt3, 'axis1') || strcmp(parser.Results.opt4, 'axis1'))
  assignin('caller', 'axis1', axis1)
end
if ismember('opt1',parser.UsingDefaults) || (strcmp(parser.Results.opt1, 'axis2') || strcmp(parser.Results.opt2, 'axis2') || strcmp(parser.Results.opt3, 'axis2') || strcmp(parser.Results.opt4, 'axis2'))
  assignin('caller', 'axis2', axis2)
end
end
