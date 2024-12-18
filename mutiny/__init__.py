# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

from _collections import OrderedDict

import os
import sys
import xarray as xr

# xarray options
xr.set_options(keep_attrs=True)

# This variable will be constantly changed depending on what x value the user is hovering over
class HoverTime(object):
    hover_time = 0
    functions_to_call = []

    def register_listener(self, fn):
        self.functions_to_call.append(fn)
        return

    # New time is time we're hovering over, grabbed from TVarFigure(1D/Spec/Alt/Map)
    # name is whatever tplot we're currently hovering over (relevant for 2D interactive
    # plots that appear when plotting a spectrogram).
    def change_hover_time(self, new_time, name=None):
        self.hover_time = new_time
        for f in self.functions_to_call:
            try:
                f(self.hover_time, name)
            except Exception as e:
                print(e)
        return

# Global Variables
hover_time = HoverTime()
data_quants = OrderedDict()
interactive_window = None  # 2D interactive window that appears whenever plotting spectrograms w/ tplot.
# If option 't_average' is set by user, then x and y values on this plot are the average of the user-specified
# number of seconds for which the cursor location should be averaged.
static_window = None  # 2D window showing data at certain point in time from a spectrogram plot.
static_tavg_window = None  # 2D window showing averaged y and z data for a specified time range from a spectrogram plot.
tplot_opt_glob = dict(tools="xpan,crosshair,reset",
                      min_border_top=12, min_border_bottom=12,
                      title_align='center', window_size=[800, 800],
                      title_size='12', title_text='', crosshair=True,
                      data_gap=0, black_background=False, axis_font_size=12, axis_tick_num=[(0, 1000000000), (3, 1),],
                      y_axis_zoom=False)
lim_info = {}
extra_layouts = {}

from .store_data import store_data, store
from .tplot import tplot, plot
from .get_data import get_data, get
from .xlim import xlim
from .ylim import ylim
from .zlim import zlim
from .tlimit import tlimit
from .tplot_names import tplot_names
from .tnames import tnames
from .is_pseudovariable import is_pseudovariable
from .count_traces import count_traces
from .get_timespan import get_timespan
from .tplot_options import tplot_options
from .tplot_rename import tplot_rename
from .tplot_copy import tplot_copy
from .replace_data import replace_data
from .replace_metadata import replace_metadata
from .get_ylimits import get_ylimits
from .timebar import timebar
from .del_data import del_data
from .timespan import timespan
from .options import options
from .timestamp import timestamp
from .time_double import time_float,time_double, time_float_one
from .time_string import time_string, time_datetime, time_string_one
from .tplot_utilities import compare_versions
from .tplot_utilities import highlight
from .tplot_utilities import annotate
from .data_att_getters_setters import set_coords, get_coords, set_units, get_units
from .data_exists import data_exists
from .link import link
from .tres import tres
from .format_sandbox import format_sandbox
from .tplot_math import *
from .wildcard_routines import wildcard_expand, tplot_wildcard_expand, tname_byindex, tindex_byname


# set up logging/console output
import logging
from os import environ

logging_level = environ.get('mutiny_LOGGING_LEVEL')
logging_format = environ.get('mutiny_LOGGING_FORMAT')
logging_date_fmt = environ.get('mutiny_LOGGING_DATE_FORMAT')

if logging_format is None:
    logging_format = '%(asctime)s: %(message)s'

if logging_date_fmt is None:
    logging_date_fmt = '%d-%b-%y %H:%M:%S'

if logging_level is None:
    logging_level = logging.INFO
else:
    logging_level = logging_level.lower()
    if logging_level == 'debug':
        logging_level = logging.DEBUG
    elif logging_level == 'info':
        logging_level = logging.INFO
    elif logging_level == 'warn' or logging_level == 'warning':
        logging_level = logging.WARNING
    elif logging_level == 'error':
        logging_level = logging.ERROR
    elif logging_level == 'critical':
        logging_level = logging.CRITICAL

logging.captureWarnings(True)

# basicConfig here doesn't work if it has previously been called
logging.basicConfig(format=logging_format, datefmt=logging_date_fmt, level=logging_level)

# manually set the logger options from the defaults/environment variables
logger = logging.getLogger()
logger_handler = logger.handlers[0]  # should exist since basicConfig has been called
logger_fmt = logging.Formatter(logging_format, logging_date_fmt)
logger_handler.setFormatter(logger_fmt)
logger.setLevel(logging_level)
