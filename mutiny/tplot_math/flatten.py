import mutiny
import copy
import logging


def flatten(tvar, range=None, newname=None, new_tvar=None):
    """
    Divides the column by an average over specified time

    .. note::
        This analysis routine assumes the data is no more than 2 dimensions.  If there are more, they may become flattened!

    Parameters
    ----------
        tvar : str
            Name of first tplot variable.
        range : [int, int], optional
            The time range to average over.  The default is the whole range.
        newname : str
            Name of new tvar for added data.  If not set, then a name is made up.
        new_tvar : str (Deprecated)
            Name of new tvar for added data.  If not set, then a name is made up.

    Returns
    -------
        None

    Examples
    --------
        >>> # Divide each column by the average of the data between times 8 and 14
        >>> mutiny.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1,50],[2,2,3],[100,4,47],[4,90,5],[5,5,99],[6,6,25],[7,7,-5]]})
        >>> mutiny.flatten('d',[8,14],'d_flatten')
        >>> print(mutiny.data_quants['d_flatten'].values)
    """
    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info(
            "flatten: The new_tvar parameter is deprecated. Please use newname instead."
        )
        newname = new_tvar

    if newname is None:
        newname = tvar + "_flattened"

    if "spec_bins" in mutiny.data_quants[tvar].coords:
        df, s = mutiny.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(tvar)
    else:
        df = mutiny.tplot_utilities.convert_tplotxarray_to_pandas_dataframe(
            tvar, no_spec_bins=True
        )
        s = None

    if range is None:
        pass

    time = df.index
    # if time given not an index, choose closest time
    if range is None:
        df_index = list(df.columns)
        # divide by column average
        for i in df_index:
            df[i] = df[i] / df[i].mean()
    else:
        if range[0] not in time:
            tdiff = abs(time - range[0])
            start_t = time[tdiff.argmin()]
        if range[1] not in time:
            tdiff = abs(time - range[1])
            end_t = time[tdiff.argmin()]
        df_index = list(df.columns)

        # divide by specified time average
        for i in df_index:
            df[i] = df[i] / ((df.loc[start_t:end_t])[i]).mean()

    if s is not None:
        mutiny.store_data(newname, data={"x": df.index, "y": df.values, "v": s.values})
        mutiny.data_quants[newname].attrs = copy.deepcopy(
            mutiny.data_quants[tvar].attrs
        )
    else:
        mutiny.store_data(newname, data={"x": df.index, "y": df.values})
        mutiny.data_quants[newname].attrs = copy.deepcopy(
            mutiny.data_quants[tvar].attrs
        )
    return
