import mutiny
import copy
import numpy as np
import logging


def deflag(tvar, flag=None, newname=None, new_tvar=None, method=None, fillval=None):
    """
    Replace NaN or other 'flag' values in arrays with interpolated or other values.

    Parameters
    ----------

        tvar: str
            Name of tplot variable to use for data clipping.
        flag : int,list
            Flagged data will be converted to NaNs.
        method : str, optional
            Method to apply. Valid options::

                'repeat': Repeat last good value
                'linear': Interpolate linearly over gap
                'replace': Replace flagged values with fillval, or NaN if fillval not specified
                'remove_nan': Remove timestamps and values with a NaN in any dimension

        newname : str
            Name of new tvar for deflagged data storage.
            If not specified, then the data in tvar1 will be replaced.
            This is not an option for multiple variable input, for
            multiple or pseudo variables, the data is overwritten.
        new_tvar : str (Deprecated)
            Name of new tvar for deflagged data storage.  
            If not specified, then the data in tvar1 will be replaced.
            THIS is not an option for multiple variable input, for 
            multiple or pseudo variables, the data is overwritten.
        fillval: int, float (optional)
            Value to use as replacement when method='replace'

    Notes
    -----

       deflag only works for 1 or 2-d data arrays; ntimes or (ntimes, nspectral_bins)

    Returns
    -------

        None

    Examples
    --------

        >>> mutiny.store_data('d', data={'x':[2,5,8,11,14,17,21], 'y':[[1,1],[2,2],[100,4],[4,90],[5,5],[6,6],[7,7]]})
        >>> # Remove any instances of [100,90,7,2,57] from 'd', store in 'e'.
        >>> mutiny.deflag('d',[100,90,7,2,57],newname='e')

    """

    # new_tvar is deprecated in favor of newname
    if new_tvar is not None:
        logging.info("deflag: The new_tvar parameter is deprecated. Please use newname instead.")
        newname = new_tvar

    # for linear method, and flag of NaN, or none, interp_nan an be called
    #    if (flag == None or np.isnan(flag)) and method == 'linear':
    #        interp_nan(tvar, newname=newname)
    #        return
    
    # check for globbed or array input, and call recursively
    tn = mutiny.tnames(tvar)
    if len(tn) > 1:
        for j in range(len(tn)):
            mutiny.deflag(tn[j], flag, method=method, fillval=fillval)
        return

    # Now flag needs to be an array
    if flag is None:
        flag = np.zeros(1)+np.nan
    else:
        if not isinstance(flag, np.ndarray):
            flag_array = np.array(flag)
        else:
            flag_array = flag
        # Ok, now if flag was a scalar, the array will have ndim = 0
        if flag_array.ndim == 0:
            flag = np.array([flag])
        else:
            flag = flag_array
    
    nf = len(flag)
    if method == 'remove_nan':  # this is different from the other methods, which retain all time intervals
        a = copy.deepcopy(mutiny.get_data(tvar))
        alen = len(a)
        # Ignore more than 2d Y input
        if alen > 3:
            logging.info('deflag is not used for more than 2-d input')
            return

        time = a[0]
        data = a[1]
        # Added this to prevent error on !-d arrays (see below)
        data_dim = data.ndim
        new_time = []
        new_data = []
        
        if alen == 3:  # v variable
            v = a[2]
            if v.ndim == 1:
                new_v = v
                append_v = False
            else:
                new_v = []
                append_v = True

        # Fill the new variable
        for j in range(len(time)):
            # This used to be "if len(data[j]) > 1", which failed if data is 1-D so that data[j] is scalar
            # Instead we go by the dimensions of the data array itself
            if data_dim > 1:
                tj = np.sum(data[j])
            else:
                tj = data[j]
            if not np.isnan(tj):
                new_time.append(time[j])
                new_data.append(data[j])
                if alen == 3 and append_v:
                    new_v.append(v[j])

        if newname is None:
            if alen == 2:
                mutiny.store_data(tvar, data={'x': new_time, 'y': new_data})
            else:
                mutiny.store_data(tvar, data={'x': new_time, 'y': new_data, 'v': new_v})
        else:
            if alen == 2:
                mutiny.store_data(newname, data={'x': new_time, 'y': new_data})
            else:
                mutiny.store_data(newname, data={'x': new_time, 'y': new_data, 'v': new_v})
            mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)
    elif method == 'repeat' or method == 'linear' or method == 'replace':
        a = copy.deepcopy(mutiny.get_data(tvar))
        time = a[0]
        data = a[1]
        alen = len(a)
        if alen > 3:
            logging.info('deflag is not used for more than 2-d input')
            return
        if alen == 3:
            v = a[2]
        ntimes = time.shape[0]
        nydim = data.ndim
        if nydim == 1:
            ny = 1
        else:
            ny = data.shape[1]
        for i in range(nf):
            if np.isnan(flag[i]):  # NaN flags need special handling
                flag_is_nan = True
            else:
                flag_is_nan = False
            for k in range(ny):
                print(data[:, k])
                if (flag_is_nan):
                    flagged_data = np.where(np.isnan(data[:, k]))[0]
                else:
                    flagged_data = np.where(data[:, k] == flag[i])[0]
                if len(flagged_data) > 0:
                    if flag_is_nan:
                        okval = np.where(np.isnan(data[:, k]) is False)[0]
                    else:
                        okval = np.where(data[:, k] != flag[i])[0]

                    if len(okval) == 0:
                        logging.info('No unflagged data, returning')
                        return
                    if method == 'repeat':  # flagged data repeats the previous unflagged value
                        for j in range(ntimes):
                            if (flag_is_nan):
                                if np.isnan(data[j, k]):
                                    if j == 0:
                                        data[j, k] = data[okval[0], k]
                                    else:
                                        data[j, k] = data[j-1, k]
                            else:
                                if data[j, k] == flag[i]:
                                    if j == 0:
                                        data[j, k] = data[okval[0], k]
                                    else:
                                        data[j, k] = data[j-1, k]
                    elif method == 'replace':
                        if fillval is None:
                            fv = np.nan
                        else:
                            fv = fillval
                        data[flagged_data, k] = fv
                    else:  # method = 'linear'
                        # interpolate flagged data, using np.interp
                        dataj = data[okval, k]
                        timej = time[okval]
                        timej_flagged = time[flagged_data]
                        dataj_interpd = np.interp(timej_flagged, timej, dataj)
                        data[flagged_data, k] = dataj_interpd
                else:
                    print("No Flagged_data")

        if newname is None:
            if alen == 2:
                mutiny.store_data(tvar, data={'x': time, 'y': data})
            else:
                mutiny.store_data(tvar, data={'x': time, 'y': data, 'v': v})
        else:
            if alen == 2:
                mutiny.store_data(newname, data={'x': time, 'y': data})
            else:
                mutiny.store_data(newname, data={'x': time, 'y': data, 'v': v})
                mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)
    else:  # any other option includes method=None, replace flags with NaN
        nf = len(flag)
        a = copy.deepcopy(mutiny.data_quants[tvar].where(mutiny.data_quants[tvar] != flag[0]))
        if nf > 1:
            for j in range(nf):
                a = copy.deepcopy(a.where(a != flag[j]))
        if newname is None:
            a.name = tvar
            mutiny.data_quants[tvar] = a
        else:
            if 'spec_bins' in a.coords:
                mutiny.store_data(newname, data={'x': a.coords['time'], 'y': a.values, 'v': a.coords['spec_bins']})
                mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)
            else:
                mutiny.store_data(newname, data={'x': a.coords['time'], 'y': a.values})
                mutiny.data_quants[newname].attrs = copy.deepcopy(mutiny.data_quants[tvar].attrs)

    return
