# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
from . import tplot_utilities
import logging

def get_timespan(name):
    """
    This function extracts the time span from the Tplot Variables stored in memory.  
    
    Parameters
    ----------
        name : str 
            Name of the tplot variable
         
    Returns
    -------
    list of float
        time_begin : float
            The beginning of the time series
        time_end : float
            The end of the time series
            
    Examples
    --------
        >>> # Retrieve the time span from Variable 1
        >>> import mutiny
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> mutiny.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> time1, time2 = mutiny.get_timespan("Variable1")

    """
    
    if name not in mutiny.data_quants.keys():
        logging.info("The name %s is currently not in mutiny",name)
        return

    return mutiny.data_quants[name].attrs['plot_options']['trange'][0], mutiny.data_quants[name].attrs['plot_options']['trange'][1]