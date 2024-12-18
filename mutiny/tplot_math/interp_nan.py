import mutiny
import copy
import logging


def interp_nan(tvar, newname=None, new_tvar=None, s_limit=None):
    """
    Interpolates the tplot variable through NaNs in the data. This is basically just a wrapper for xarray's interpolate_na function.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions. If there are more, they may become flattened!

    Parameters
    ----------
    tvar : str
        Name of tplot variable.
    newname : str
        Name of new tvar for added data. If not set, then the original tvar is replaced.
    new_tvar : str (Deprecated)
        Name of new tvar for added data. If not set, then the original tvar is replaced.
    s_limit : int or float, optional
        The maximum size of the gap in seconds to not interpolate over. I.e. if there are too many NaNs in a row, leave them there.

    Returns
    -------
    None

    Examples
    --------
    >>> import mutiny
    >>> import numpy as np
    >>> mutiny.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
    >>> mutiny.interp_nan('e','e_nonan',s_limit=5)
    >>> print(mutiny.data_quants['e_nonan'].values)
    """
    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info(
            "interp_nan: The new_tvar parameter is deprecated. Please use newname instead."
        )
        newname = new_tvar

    x = mutiny.data_quants[tvar].interpolate_na(dim="time", limit=s_limit)
    x.attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)

    if newname is None:
        mutiny.data_quants[tvar] = x
        x.name = tvar
    else:
        mutiny.data_quants[newname] = x
        mutiny.data_quants[newname].name = newname
