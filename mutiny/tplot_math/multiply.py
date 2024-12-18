import mutiny
import copy
import logging


def multiply(tvar1, tvar2, newname=None, new_tvar=None):
    """
    Multiplies two tplot variables.  Will interpolate if the two are not on the same time cadence.

    Parameters
    ----------
        tvar1 : str
            Name of first tplot variable.
        tvar2 : int/float
            Name of second tplot variable.
        newname : str
            Name of new tplot variable.  If not set, then the data in tvar1 is replaced.
        new_tvar : str (Deprecated)
            Name of new tplot variable.  If not set, then the data in tvar1 is replaced.

    Returns
    -------
        None

    Examples
    --------
        >>> x1 = [0, 4, 8, 12, 16]
        >>> x2 = [0, 4, 8, 12, 16, 19, 21]
        >>> time1 = [mutiny.time_float("2020-01-01") + i for i in x1]
        >>> time2 = [mutiny.time_float("2020-01-01") + i for i in x2]
        >>> mutiny.store_data("a", data={"x": time1, "y": [1, 2, 3, 4, 5]})
        >>> mutiny.store_data("c", data={"x": time2, "y": [1, 4, 1, 7, 1, 9, 1]})
        >>> n = mutiny.multiply("a", "c", newname="a_x_c")
        >>> print('new tplot variable:', n)
        >>> ac = mutiny.get_data(n)
        >>> print(ac)
    """
    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info(
            "multiply: The new_tvar parameter is deprecated. Please use newname instead."
        )
        newname = new_tvar

    # interpolate tvars
    tv2 = mutiny.tplot_math.tinterp(tvar1, tvar2)
    # separate and multiply data
    data1 = mutiny.data_quants[tvar1].values
    data2 = mutiny.data_quants[tv2].values
    data = data1 * data2

    if newname is None:
        mutiny.data_quants[tvar1].values = data
        return tvar1

    if "spec_bins" in mutiny.data_quants[tvar1].coords:
        mutiny.store_data(
            newname,
            data={
                "x": mutiny.data_quants[tvar1].coords["time"].values,
                "y": data,
                "v": mutiny.data_quants[tvar1].coords["spec_bins"].values,
            },
        )
        mutiny.data_quants[newname].attrs = copy.deepcopy(
            mutiny.data_quants[tvar1].attrs
        )
    else:
        mutiny.store_data(
            newname,
            data={"x": mutiny.data_quants[tvar1].coords["time"].values, "y": data},
        )
        mutiny.data_quants[newname].attrs = copy.deepcopy(
            mutiny.data_quants[tvar1].attrs
        )
    return newname
