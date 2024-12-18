# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
import copy


def tinterp(tvar1,tvar2,replace=False):
    """
    Interpolates one tplot variable to another one's time cadence.  This is done automatically by other processing routines.

    Parameters
    ----------
        tvar1 : str
            Name of first tplot variable whose times will be used to interpolate tvar2's data.
        tvar2 : str
            Name of second tplot variable whose data will be interpolated.
        replace : bool, optional
            If true, the data in the original tplot variable is replaced.  Otherwise, a variable is created.

    Returns
    -------
        str
            Name of the new tplot variable

    Examples
    --------
        >>> mutiny.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> mutiny.store_data('c', data={'x':[0,4,8,12,16,19,21], 'y':[1,4,1,7,1,9,1]})
        >>> mutiny.tinterp('a','c')
        >>> print(mutiny.data_quants['c_interp'].data)
    """
    new_tvar2 = mutiny.data_quants[tvar2].interp_like(mutiny.data_quants[tvar1])

    if replace:
        mutiny.data_quants[tvar2] = new_tvar2
        return
    else:
        mutiny.data_quants[tvar1 + '_tinterp'] = copy.deepcopy(new_tvar2)
        mutiny.data_quants[tvar1 + '_tinterp'].attrs = copy.deepcopy(new_tvar2.attrs)
        mutiny.data_quants[tvar1 + '_tinterp'].name = tvar1 + '_tinterp'

    return tvar1 + '_tinterp'
