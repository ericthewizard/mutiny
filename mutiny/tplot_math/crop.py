# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
import copy

def crop(tvar1,tvar2, replace=True):
    """
    Crops both tplot variable so that their times are the same.  This is done automatically by other processing routines if times do not match up.

    Parameters
    -----------
        tvar1 : str
            Name of the first tplot variable
        tvar2 : str
            Name of the second tplot variable
        replace : bool, optional
            If true, the data in the original tplot variables are replaced.  Otherwise, new variables are created.

    Returns
    -------
        None


    Examples
    --------

        >>> mutiny.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> mutiny.store_data('b', data={'x':[2,5,8,11,14,17,20], 'y':[[1,1,1,1,1,1],[2,2,5,4,1,1],[100,100,3,50,1,1],[4,4,8,58,1,1],[5,5,9,21,1,1],[6,6,2,2,1,1],[7,7,1,6,1,1]]})
        >>> mutiny.crop('a','b')
        >>> print(mutiny.data_quants['a'].data)
        >>> print(mutiny.data_quants['b'].data)
    """

    # grab time and data arrays
    tv1 = mutiny.data_quants[tvar1].copy()
    tv2 = mutiny.data_quants[tvar2].copy()
    # find first and last time indices
    t0_1 = tv1.coords['time'][0]
    t0_2 = tv2.coords['time'][0]
    tx_1 = tv1.coords['time'][-1]
    tx_2 = tv2.coords['time'][-1]
    # find cut locations
    cut1 = max([t0_1, t0_2])
    cut2 = min([tx_1, tx_2])
    # trim data
    tv1 = tv1.sel(time=slice(cut1, cut2))
    tv1.attrs = copy.deepcopy(mutiny.data_quants[tvar1].attrs)
    tv2 = tv2.sel(time=slice(cut1, cut2))
    tv2.attrs = copy.deepcopy(mutiny.data_quants[tvar2].attrs)
    # Replace the variables if specified
    if replace:
        mutiny.data_quants[tvar1] = tv1
        mutiny.data_quants[tvar1].name = tvar1
        mutiny.data_quants[tvar2] = tv2
        mutiny.data_quants[tvar2].name = tvar2
        return
    else:
        mutiny.data_quants[tvar1 + '_cropped'] = copy.deepcopy(tv1)
        mutiny.data_quants[tvar1 + '_cropped'].attrs = copy.deepcopy(tv1.attrs)
        mutiny.data_quants[tvar1 + '_cropped'].name = tvar1+ '_cropped'
        mutiny.data_quants[tvar2 + '_cropped'] = copy.deepcopy(tv2)
        mutiny.data_quants[tvar2 + '_cropped'].attrs = copy.deepcopy(tv2.attrs)
        mutiny.data_quants[tvar2 + '_cropped'].name = tvar2 + '_cropped'
    return tvar2 + '_cropped'