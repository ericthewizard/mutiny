# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

from __future__ import division
import mutiny

from .xlim import xlim


def tlimit(arg=None, full=False, last=False):
    """

    Parameters
    ----------
    arg: str or list
        If arg=='full', revert to the full time range. If arg=='last', revert to the previous time range.
        Otherwise, arg should be a list containing a start and stop time.
    full: bool
        If True, revert to the full time range. Equivalent to tlimit('full').
    last: bool:
        If True, revert to the previous time range. Equivalent to tlimit('last').

    Returns
    -------
        None

    Examples
    --------
    >>> import mutiny
    >>> mutiny.tlimit(['2023/03/24/', '2023/03/25'])

    """

    if full or arg == 'full':
        if mutiny.tplot_opt_glob.get('x_range') is not None:
            del mutiny.tplot_opt_glob['x_range']
    elif last or arg == 'last':
        mutiny.tplot_opt_glob['x_range'] = mutiny.tplot_opt_glob['x_range_last']
    elif isinstance(arg, list):
        minn = arg[0]
        maxx = arg[1]
        xlim(minn, maxx)
        
    return
