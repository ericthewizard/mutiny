# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
from . import tplot_utilities

def xlim(min, max):
    """
    This function will set the x axis range for all time series plots
    
    Parameters
    ----------
        min : flt
            The time to start all time series plots.  Can be given in seconds since epoch, or as a string
            in the format "YYYY-MM-DD HH:MM:SS"
        max : flt
            The time to end all time series plots.  Can be given in seconds since epoch, or as a string
            in the format "YYYY-MM-DD HH:MM:SS" 
            
    Returns
    -------
        None
    
    Examples:
    ---------
        >>> # Set the timespan to be 2017-07-17 00:00:00 plus 1 day
        >>> import mutiny
        >>> mutiny.xlim(1500249600, 1500249600 + 86400)
        
        >>> # The same as above, but using different inputs
        >>> mutiny.xlim("2017-07-17 00:00:00", "2017-07-18 00:00:00")

    """
    if not isinstance(min, (int, float, complex)):
        min = tplot_utilities.str_to_float_fuzzy(min)
    if not isinstance(max, (int, float, complex)):
        max = tplot_utilities.str_to_float_fuzzy(max)
    if 'x_range' in mutiny.tplot_opt_glob:
        mutiny.tplot_opt_glob['x_range_last'] = mutiny.tplot_opt_glob['x_range']
        mutiny.lim_info['xlast'] = mutiny.tplot_opt_glob['x_range']
    else:
        mutiny.tplot_opt_glob['x_range_full'] = [min, max]
        mutiny.lim_info['xfull'] = [min, max]
        mutiny.lim_info['xlast'] = [min, max]
    mutiny.tplot_opt_glob['x_range'] = [min, max]
    return
