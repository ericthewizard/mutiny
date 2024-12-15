# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutinyplot

import mutinyplot
import datetime


def timestamp(val):
    """
    This function will turn on a time stamp that shows up at the bottom of every generated plot.

    Parameters
    ----------
        val  str
            A string that can either be 'on' or 'off'.

    Returns
        None

    Examples
    --------
         >>> # Turn on the timestamp
         >>> import mutinyplot
         >>> mutinyplot.timestamp('on')
    """

    if val == 'on':
        todaystring = datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
        mutinyplot.extra_layouts['time_stamp'] = todaystring
    else:
        if 'time_stamp' in mutinyplot.extra_layouts:
            del mutinyplot.extra_layouts['time_stamp']

    return
