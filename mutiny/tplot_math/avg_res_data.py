import mutiny
import numpy as np
import copy
import logging

def avg_res_data(tvar,res,newname=None,new_tvar=None):
    """
    Averages the variable over a specified period of time.

    Parameters
    ----------
        tvar1 : str
            Name of tplot variable.
        res : int/float
            The new data resolution
        new_tvar : str (Deprecated)
            Name of new tvar for averaged data.  If not set, then the data in tvar is replaced.
        newname : str
            Name of new tvar for averaged data.  If not set, then the data in tvar is replaced.

    Returns
    -------
        None

    Note
    ----

    This routine uses the xarray coarsen() method to reduce the time resolution.  It will only work if the
    data is evenly gridded, and the res parameter evenly divides the number of samples.
    For most purposes, it is more appropriate to use pyspedas.avg_data() instead.

    Examples
    --------

        >>> #Average the data over every two seconds
        >>> mutiny.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> mutiny.avg_res_data('d',2,'d2res')
        >>> print(mutiny.data_quants['d'].values)
    """

    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info("avg_res_data: The new_tvar parameter is deprecated. Please use newname instead.")
        newname = new_tvar

    tvar_new = mutiny.data_quants[tvar].coarsen(time=res, boundary='trim').mean()
    tvar_new.name = mutiny.data_quants[tvar].name
    tvar_new.attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)

    if newname is None:
        mutiny.data_quants[tvar] = newname
    else:
        if 'spec_bins' in mutiny.data_quants[tvar].coords:
            mutiny.store_data(newname, data={'x': tvar_new.coords['time'].values, 'y': tvar_new.values,
                                               'v': tvar_new.coords['spec_bins'].values})
        else:
            mutiny.store_data(newname, data={'x': tvar_new.coords['time'].values, 'y': tvar_new.values})

        mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)

    return

