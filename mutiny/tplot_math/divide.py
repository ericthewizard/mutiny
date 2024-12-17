# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
import numpy as np
import copy
import logging

def divide(tvar1,tvar2,newname=None, new_tvar=None):
    """
    Divides two tplot variables.  Will interpolate if the two are not on the same time cadence.

    Parameters
    ----------
        tvar1 : str
            Name of first tplot variable.
        tvar2 : int/float
            Name of second tplot variable
        new_tvar : str (Deprecated)
            Name of new tvar for divided data.  If not set, then the data in tvar1 is replaced.
        newname : str
            Name of new tvar for divided data.  If not set, then the data in tvar1 is replaced.

    Returns
    -------
        None

    Examples
    --------

        >>> mutiny.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> mutiny.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
        >>> mutiny.divide('a','c','a_over_c')
        """
    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info("divide: The new_tvar parameter is deprecated. Please use newname instead.")
        newname = new_tvar

    # interpolate tvars
    tv2 = mutiny.tplot_math.tinterp(tvar1, tvar2)
    # separate and divide data
    data1 = mutiny.data_quants[tvar1].values
    data2 = mutiny.data_quants[tv2].values
    data = data1 / data2
    # store divided data
    if newname is None:
        mutiny.data_quants[tvar1].values = data
        return tvar1
    if 'spec_bins' in mutiny.data_quants[tvar1].coords:
        mutiny.store_data(newname, data={'x': mutiny.data_quants[tvar1].coords['time'].values, 'y': data,
                                           'v': mutiny.data_quants[tvar1].coords['spec_bins'].values})
        mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar1].attrs)
    else:
        mutiny.store_data(newname, data={'x': mutiny.data_quants[tvar1].coords['time'].values, 'y': data})
        mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar1].attrs)

    return new_tvar
