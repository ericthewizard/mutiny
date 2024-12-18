import mutiny
import pandas as pd
import copy
import xarray as xr
import logging


# JOIN TVARS
# join TVars into single TVar with multiple columns
def join_vec(tvars, newname=None, new_tvar=None, merge=False):
    """
    Joins 1D tplot variables into one tplot variable.

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions. If there are more, they may become flattened!

    Parameters
    ----------
    tvars : list of str
        Name of tplot variables to join together.
    newname : str, optional
        The name of the new tplot variable. If not specified (the default), a name will be assigned.
    new_tvar : str, optional (Deprecated)
        The name of the new tplot variable. If not specified, a name will be assigned.
    merge : bool, optional
        Whether or not to merge the created variable into an older variable.
        Default is False.

    Returns
    -------
    None

    Examples
    --------
    >>> import mutiny
    >>> import numpy as np
    >>> mutiny.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
    >>> mutiny.store_data('e', data={'x':[2,5,8,11,14,17,21], 'y':[[np.nan,1,1],[np.nan,2,3],[4,np.nan,47],[4,np.nan,5],[5,5,99],[6,6,25],[7,np.nan,-5]]})
    >>> mutiny.store_data('g', data={'x':[0,4,8,12,16,19,21], 'y':[[8,1,1],[100,2,3],[4,2,47],[4,39,5],[5,5,99],[6,6,25],[7,-2,-5]]})
    >>> mutiny.join_vec(['d','e','g'],newname='deg')
    >>> print(mutiny.data_quants['deg'].values)
    """
    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info(
            "join_vec: The new_tvar parameter is deprecated. Please use newname instead."
        )
        newname = new_tvar

    if not isinstance(tvars, list):
        tvars = [tvars]
    if newname is None:
        newname = "-".join(tvars) + "_joined"

    to_merge = False
    if newname in mutiny.data_quants.keys() and merge:
        prev_data_quant = mutiny.data_quants[newname]
        to_merge = True

    for i, val in enumerate(tvars):
        if i == 0:
            if "spec_bins" in mutiny.data_quants[tvars[i]].coords:
                df, s = mutiny.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(
                    tvars[i]
                )
            else:
                df = mutiny.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(
                    tvars[i], no_spec_bins=True
                )
                s = None
        else:
            if "spec_bins" in mutiny.data_quants[tvars[i]].coords:
                d = mutiny.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(
                    tvars[i], no_spec_bins=True
                )
            else:
                d = mutiny.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(
                    tvars[i], no_spec_bins=True
                )
            df = pd.concat([df, d], axis=1)

    if s is None:
        mutiny.store_data(newname, data={"x": df.index, "y": df.values})
    else:
        mutiny.store_data(newname, data={"x": df.index, "y": df.values, "v": s.values})

    if to_merge is True:
        cur_data_quant = mutiny.data_quants[newname]
        plot_options = copy.deepcopy(mutiny.data_quants[newname].attrs)
        mutiny.data_quants[newname] = xr.concat(
            [prev_data_quant, cur_data_quant], dim="time"
        ).sortby("time")
        mutiny.data_quants[newname].attrs = plot_options

    return newname
