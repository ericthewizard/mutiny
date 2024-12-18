# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

from __future__ import division
import pandas as pd
import numpy as np
import datetime
import logging
from .del_data import del_data
import mutiny
import xarray as xr
from mutiny import tplot_utilities as utilities
import copy
import warnings

tplot_num = 1


def store_data(name, data=None, delete=False, newname=None, attr_dict={}):
    
    """
    Create a "Tplot Variable" (similar to the IDL SPEDAS concept) based on the inputs, and
    stores this data in memory.  Tplot Variables store all of the information
    needed to generate a plot.  
    
    Parameters
    ----------
        name : str 
            Name of the tplot variable that will be created
        data : dict or list[str]
            A python dictionary object for creating a single variable, or a list of base variables to combine them into a 'pseudovariable'
            
            'x' should be a 1-dimensional array that represents the data's x axis.  If x is a numeric type, it is interpreted
            as seconds since the Unix epoch.  x can also be passed as Pandas Series object, datetime.datetime, numpy.datetime64, or strings.
            represented in seconds since epoch (January 1st 1970)
            
            'y' should be the data values. This can be 2 dimensions if multiple lines or a spectrogram are desired.
            
            'v' is optional, and is only used for spectrogram plots.  This will be a list of bins to be used.  If this
            is provided, then 'y' should have dimensions of x by z.

            'v1/v2/v3/etc' are also optional, and are only used for to spectrogram plots.  These will act as the coordinates
            for 'y' if 'y' has numerous dimensions.  By default, 'v2' is plotted in spectrogram plots.

        delete : bool, optional
            If True, deletes the tplot variable matching the "name" parameter
            Default: False
        newname: str
            If set, renames TVar to new name
            Default: False
        attr_dict: dict
            A dictionary object of attributes (these do not affect routines in mutiny, this is merely to keep metadata alongside the file)
            Default: {} (empty dictionary)
        
    .. note::
        If you want to combine multiple tplot variables into one, simply supply the list of tplot variables to the
        "data" parameter.  This will cause the data to overlay when plotted.
        
    Returns
    -------
        bool
            True if successful, False otherwise
        
    Examples
    --------
        >>> # Store a single line
        >>> import mutiny
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> mutiny.store_data("Variable1", data={'x':x_data, 'y':y_data})
    
        >>> # Store two lines
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> mutiny.store_data("Variable2", data={'x':x_data, 'y':y_data})
        
        >>> # Store a spectrogram
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> mutiny.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        
        >>> # Combine two different line plots
        >>> mutiny.store_data("Variable1and2", data=['Variable1', 'Variable2'])
        
        >>> #Rename TVar
        >>> mutiny.store_data('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> mutiny.store_data('a',newname='f')

    """
    
    global tplot_num
    create_time = datetime.datetime.now()
    # If delete is specified, we are just deleting the variable
    if delete is True:
        del_data(name)
        return False

    if data is None and newname is None:
        logging.error('store_data: Neither data array nor newname supplied, nothing to do.')
        return False

    # If newname is specified, we are just renaming the variable
    if newname is not None:
        mutiny.tplot_rename(name, newname)
        return True

    # if isinstance(data, str):
    #     mutiny.data_quants[name] = {'name': name, 'data': data}
    #     return True
    if isinstance(data, str):
        data = data.split(' ')

    # If the data is a list instead of a dictionary, user is looking to overplot
    if isinstance(data, list):
        base_data = _get_base_tplot_vars(name,data)
        if len(base_data) == 0:
            logging.warning("store_data: None of the base variables exist to construct pseudovariable %s",name)
            return False
        # Copying the first variable to use all of its plot options
        # However, we probably want each overplot to retain its original plot option
        mutiny.data_quants[name] = copy.deepcopy(mutiny.data_quants[base_data[0]])
        mutiny.data_quants[name].attrs = copy.deepcopy(mutiny.data_quants[base_data[0]].attrs)
        mutiny.data_quants[name].name = name
        mutiny.data_quants[name].attrs['plot_options']['overplots'] = base_data[1:]
        mutiny.data_quants[name].attrs['plot_options']['overplots_mpl'] = base_data
        # These sets of options should default to the sub-variables' options, not simply
        # copied from the first variable in the list.   These options can be still be set
        # on the pseudovariable, and they will override the sub-variable options.
        mutiny.data_quants[name].attrs['plot_options']['yaxis_opt'] = {}
        mutiny.data_quants[name].attrs['plot_options']['zaxis_opt'] = {}
        mutiny.data_quants[name].attrs['plot_options']['line_opt'] = {}
        mutiny.data_quants[name].attrs['plot_options']['extras'] = {}
        return True

    # if the data table doesn't contain an 'x', assume this is a non-record varying variable
    if 'x' not in data.keys():
        values = np.array(data.pop('y'))
        mutiny.data_quants[name] = {'data': values}
        mutiny.data_quants[name]['name'] = name
        return True

    times = data.pop('x')

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        values = np.array(data.pop('y'))

    if 'dy' in data.keys():
        err_values = np.array(data.pop('dy'))

        if len(err_values) != len(times):
            logging.warning('store_data: Warning: %s: length of error values (%d) does not match length of time values (%d)',name,len(err_values),
                            len(times))
    else:
        err_values = None

    # Convert input time representation to np.datetime64 objects, if needed
    if isinstance(times, pd.core.series.Series):
        datetimes = times.to_numpy()  # if it is pandas series, convert to numpy array
    elif isinstance(times[0],(datetime.datetime,np.datetime64)):
        # Timezone-naive datetime or np.datetime64, use as-is, but we might have to convert the container to a numpy array
        if isinstance(times,np.ndarray):
            datetimes = times
        else:
            datetimes = np.array(times)
    elif isinstance(times[0],(int,np.integer,float,np.float64)):
        # Assume seconds since Unix epoch, convert to np.datetime64 with nanosecond precision
        # Make sure we have a numpy array
        if not isinstance(times,np.ndarray):
            times=np.array(times)
        # Replace any NaN or inf values with 0
        cond = np.logical_not(np.isfinite(times))
        times[cond] = 0
        datetimes = np.array(times*1e09,dtype='datetime64[ns]')
    elif isinstance(times[0],str):
        # Interpret strings as timestamps, convert to np.datetime64 with nanosecond precision
        datetimes = np.array(times,dtype='datetime64[ns]')
    else:
        # Hope it's convertable to a numpy array!  This case will get hit for an xarray DataArray.
        datetimes = np.array(times)

    times = datetimes

    # At this point, times should be a numpy array of datetime or np.datetime64 objects

    if len(values.shape) == 0:
        # This can happen for Cluster variables with only a single sample, as they can
        # be incorrectly marked as NRV and lose their leading (time) dimension.
        logging.warning("store_data: Data array for %s appears to be a zero-dimensional array; converting to 1-D array.",name)
        if len(times) == 1:
            logging.warning("store_data: This is possibly due to the leading array dimension being lost in a scalar variable with a single timestamp.")
        values = np.array([values])

    if len(values) == 0:
        logging.warning('store_data: %s has empty y component, cannot create variable',name)
        return False

    if len(times) != len(values):
        # This happens for a few MMS and other data sets. Rather than quitting immediately, go ahead and create
        # the variable, but give an informational message about the mismatch.  The fix would probably be for the
        # data provider to mark the variable as non-record-variant, and avoid giving it a DEPEND_0 or DEPEND_TIME
        # attribute.
        logging.info("store_data: %s: lengths of x (%d) and y (%d) do not match! Mislabeled NRV variable?",name,len(times),len(values))

    if not isinstance(times,np.ndarray):
        logging.warning("store_data: times was not converted to a numpy array. This should not happen.")
        times = np.array(times)

    # assumes monotonically increasing time series
    if isinstance(times[0], datetime.datetime):
        # This may be dead code now?
        trange = [times[0].replace(tzinfo=datetime.timezone.utc).timestamp(),
                  times[-1].replace(tzinfo=datetime.timezone.utc).timestamp()]
    elif isinstance(times[0], np.datetime64):
        trange = np.float64([times[0], times[-1]]) / 1e9
    else:
        trange = [times[0], times[-1]]

    # Figure out the 'v' data
    # This seems to be conflating specplot bins with general DEPEND_N attributes.
    # Maybe only do this stuff if it's marked as a spectrum?  But what if it's from
    # a NetCDF rather than a CDF?
    spec_bins_exist = False
    if 'v' in data or 'v1' in data or 'v2' in data or 'v3' in data:
        # Generally the data is 1D, but occasionally
        # the bins will vary in time.
        spec_bins_exist = True
        if 'v' in data:
            spec_bins = data['v']
            spec_bins_dimension = 'v'
        elif ("v1" in data) and ("v2" in data) and ("v3" in data):
            spec_bins = data['v2']
            spec_bins_dimension = 'v2'
        elif ("v1" in data) and ("v2" in data):
            spec_bins = data['v2']
            spec_bins_dimension = 'v2'
        else:
            # At least one vn is missing.
            logging.warning("At least one Vn tag is missing, cannot create spec_bins from variable %s.", name)
            spec_bins_exist = False

        if spec_bins_exist and type(spec_bins) is not pd.DataFrame:
            try:
                spec_bins = pd.DataFrame(spec_bins)
            except:
                if spec_bins_dimension=='v':
                    spec_bins = np.arange(1, len(values[0])+1)
                elif spec_bins_dimension=="v2":
                    spec_bins = np.arange(1, len(values[0][0]) + 1)
                elif spec_bins_dimension=="v3":
                    spec_bins = np.arange(1, len(values[0][0][0]) + 1)
                spec_bins = pd.DataFrame(spec_bins)


        if spec_bins_exist and len(spec_bins.columns) != 1:
            # The spec_bins are time varying
            # Or maybe they're just DEPEND_N and nothing to do with spectra?
            spec_bins_time_varying = True
            if len(spec_bins) != len(times):
                # Maybe it's not a spectrum at all?
                # Cluster pressure tensor variablea havw a DEPEND_1 that's 2-D, 1x3 [['x','y','z']]
                logging.error("store_data: Length of spec_bins (%d) and times (%d) do not match for variable %s.",len(spec_bins),len(times),name)
                spec_bins = None
                spec_bins_exist = False
        elif spec_bins_exist:
            spec_bins = spec_bins.transpose()
            spec_bins_time_varying = False
    else:
        spec_bins = None
        # Provide another dimension if values are more than 1 dimension
        if len(values.shape) == 2:
            data['v'] = None
        if len(values.shape) > 2:
            data['v1'] = None
            data['v2'] = None
        if len(values.shape) > 3:
            data['v3'] = None

    # Set up xarray dimension and coordinates
    coordinate_list = sorted(list(data.keys()))
    dimension_list = [d + '_dim' for d in coordinate_list]

    if len(coordinate_list) < len(values.shape)-1:
        logging.warning("store_data: Data array for variable %s has %d dimensions, but only %d v_n keys plus time. Adding empty v_n keys.", name, len(values.shape), len(coordinate_list))
        if len(values.shape) == 2:
            data['v'] = None
        elif len(values.shape) == 3:
            if 'v' in data:
                vdat = data.pop('v')
                data['v1'] = vdat
            elif 'v1' in data:
                pass
            if 'v1' not in data:
                data['v1'] = None
            if 'v2' not in data:
                data['v2'] = None
        elif len(values.shape) == 4:
            # ERG LEPI 3dflux quality flags have this issue
            if 'v' in data:
                vdat = data.pop('v')
                data['v1'] = vdat
            elif 'v1' in data:
                pass
            if 'v1' not in data:
                data['v1'] = None
            if 'v2' not in data:
                data['v2'] = None
            if 'v3' not in data:
                data['v3'] = None

        coordinate_list = sorted(list(data.keys()))
        dimension_list = [d + '_dim' for d in coordinate_list]
        # Don't try to use these dimensions as coordinates
        spec_bins_exist = False
        spec_bins = None

    temp = None
    # Ignore warnings about cdflib non-nanosecond precision timestamps for now
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",message="^.*non-nanosecond precision.*$")
        try:
            temp = xr.DataArray(values, dims=['time']+dimension_list,
                                coords={'time': ('time', times)})
        except ValueError as err:
            logging.warning("store_data: ValueError trying to set xarray coordinates for variable %s: %s", name, str(err))
            spec_bins_exist = False
            spec_bins = None
            if len(times) == 1:
                logging.warning("store_data: This is possibly due to the leading data dimension being lost in an array-valued or vector-valued variable with a single timestamp.")
            # If data is 1-dimensional, ignore any DEPEND_N supplied
            elif (len(values.shape) == 1) and len(dimension_list) > 0:
                logging.warning("store_data: variable %s is 1-dimensional, but has additional keys defined: %s.  Dropping redundant coordinate(s).",name, dimension_list)
                temp = xr.DataArray(values, dims=['time'], coords={'time': ('time', times)})
                coordinate_list=[]
                dimension_list=[]
            else:
                logging.warning("Giving up on this variable.")
                return

    if temp is None:
        # This can happen with mismatched times/data values, and no valid DEPEND_N.
        # For example, POLAR MFE data, variable MF_Num
        logging.warning("store_data: Unable to create xarray object for variable %s, giving up.", name)
        return

    if spec_bins_exist:
        try:
            if spec_bins_time_varying:
                temp.coords['spec_bins'] = (('time', spec_bins_dimension+'_dim'), spec_bins.values)
            else:
                temp.coords['spec_bins'] = (spec_bins_dimension+'_dim', np.squeeze(spec_bins.values))
        except ValueError as err:
            logging.warning('store_data: conflicting size for at least one dimension for variable %s', name)
            logging.warning('store_data: ValueError exception text: %s',str(err))

    for d in coordinate_list:
        if data[d] is None:
            continue
        try:
            d_dimension = pd.DataFrame(data[d])
            if len(d_dimension.columns) != 1:
                if len(d_dimension) != len(times):
                    logging.warning("store_data: Length of %s (%d) and time (%d) do not match.  Cannot create coordinate for %s.",d,len(d_dimension),len(times),name)
                    continue
                temp.coords[d] = (('time', d+'_dim'), d_dimension.values)
            else:
                d_dimension = d_dimension.transpose()
                squeezed_array = np.squeeze(d_dimension.values)# np.squeeze() does something funny here if this dimension has length 1, causing a ValueError exception
                if d_dimension.size == 1:
                    logging.warning("store_data: Dimension %s of variable %s has length 1",d,name)
                    temp.coords[d] = (d+'_dim', d_dimension.values[0])
                else:
                    temp.coords[d] = (d+'_dim', squeezed_array)
        except ValueError as err:
            logging.warning("store_data: Could not create coordinate %s_dim for variable %s",d, name)
            logging.warning("store_data: ValueError exception text: %s", str(err))

    # Set up Attributes Dictionaries
    xaxis_opt = dict(axis_label='Time')
    yaxis_opt = dict(axis_label=name) if (spec_bins is None) else dict(axis_label='')
    zaxis_opt = dict(axis_label='Z-Axis') if (spec_bins is None) else dict(axis_label=name)
    xaxis_opt['crosshair'] = 'X'
    yaxis_opt['crosshair'] = 'Y'
    zaxis_opt['crosshair'] = 'Z'
    xaxis_opt['x_axis_type'] = 'linear'
    yaxis_opt['y_axis_type'] = 'linear'
    zaxis_opt['z_axis_type'] = 'linear'
    line_opt = {}
    time_bar = []
    extras = dict(panel_size=1, border=True)
    links = {}

    # Add dicts to the xarray attrs
    temp.name = name
    temp.attrs = copy.deepcopy(attr_dict)

    if 'plot_options' not in temp.attrs.keys():
        temp.attrs['plot_options'] = {}
        temp.attrs['plot_options']['xaxis_opt'] = xaxis_opt
        temp.attrs['plot_options']['yaxis_opt'] = yaxis_opt
        temp.attrs['plot_options']['zaxis_opt'] = zaxis_opt
        temp.attrs['plot_options']['line_opt'] = line_opt
        temp.attrs['plot_options']['trange'] = trange
        temp.attrs['plot_options']['time_bar'] = time_bar
        temp.attrs['plot_options']['extras'] = extras
        temp.attrs['plot_options']['create_time'] = create_time
        temp.attrs['plot_options']['links'] = links
        #temp.attrs['plot_options']['spec_bins_ascending'] = _check_spec_bins_ordering(times, spec_bins)
        temp.attrs['plot_options']['overplots'] = []
        temp.attrs['plot_options']['overplots_mpl'] = []
        temp.attrs['plot_options']['interactive_xaxis_opt'] = {}
        temp.attrs['plot_options']['interactive_yaxis_opt'] = {}
        temp.attrs['plot_options']['error'] = err_values

    mutiny.data_quants[name] = temp

    mutiny.data_quants[name].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(temp)

    return True


def _get_base_tplot_vars(name,data):
    base_vars = []
    if not isinstance(data, list):
        data = [data]
    for var in data:
        if var not in mutiny.data_quants:
            logging.warning('store_data: Pseudovariable %s component %s not found, skipping', name, var)
        elif isinstance(mutiny.data_quants[var].data, list):
            base_vars += _get_base_tplot_vars(name,mutiny.data_quants[var].data)
        else:
            base_vars += [var]
    return base_vars


def _check_spec_bins_ordering(times, spec_bins):
    """
    This is a private function, this is run during
    object creation to check if spec_bins are ascending or descending
    """
    if spec_bins is None:
        return
    if len(spec_bins) == len(times):
        break_top_loop = False
        for index, row in spec_bins.iterrows():
            if row.isnull().values.all():
                continue
            else:
                for i in row.index:
                    if np.isfinite(row[i]) and np.isfinite(row[i + 1]):
                        ascending = row[i] < row[i + 1]
                        break_top_loop = True
                        break
                    else:
                        continue
                if break_top_loop:
                    break
    else:
        ascending = spec_bins[0].iloc[0] < spec_bins[1].iloc[0]
    return ascending


def store(name, data=None, delete=False, newname=None, metadata={}):
    """
    Create tplot variables. This is a wrapper for store_data, with the only apparent
    difference being that 'attr_dict' in store_data is replaced with 'metadata' in store().
    This wrapper will likely be removed in a future release.
    Parameters:
        name : str
            Name of the tplot variable that will be created
        data : dict
            A python dictionary object.

            'x' should be a 1-dimensional array that represents the data's x axis.  Typically this data is time,
            represented in seconds since epoch (January 1st 1970)

            'y' should be the data values. This can be 2 dimensions if multiple lines or a spectrogram are desired.

            'v' is optional, and is only used for spectrogram plots.  This will be a list of bins to be used.  If this
            is provided, then 'y' should have dimensions of x by z.

            'v1/v2/v3/etc' are also optional, and are only used for to spectrogram plots.  These will act as the coordinates
            for 'y' if 'y' has numerous dimensions.  By default, 'v2' is plotted in spectrogram plots.

            'x' and 'y' can be any data format that can be read in by the pandas module.  Python lists, numpy arrays,
            or any pandas data type will all work.
        delete : bool, optional
            Deletes the tplot variable matching the "name" parameter
        newname: str
            Renames TVar to new name
        metadata: dict
            A dictionary object of attributes (these do not affect routines in mutiny, this is merely to keep metadata alongside the file)

    .. note::
        If you want to combine multiple tplot variables into one, simply supply the list of tplot variables to the
        "data" parameter.  This will cause the data to overlay when plotted.

    Returns:
        None

    Examples:
        >>> # Store a single line
        >>> import mutiny
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> mutiny.store("Variable1", data={'x':x_data, 'y':y_data})

        >>> # Store a two lines
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [[1,5],[2,4],[3,3],[4,2],[5,1]]
        >>> mutiny.store("Variable2", data={'x':x_data, 'y':y_data})

        >>> # Store a spectrogram
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> mutiny.store("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})

        >>> # Combine two different line plots
        >>> mutiny.store("Variable1and2", data=['Variable1', 'Variable2'])

        >>> #Rename TVar
        >>> mutiny.store('a', data={'x':[0,4,8,12,16], 'y':[1,2,3,4,5]})
        >>> mutiny.store('a',newname='f')
    """
    return store_data(name, data=data, delete=delete, newname=newname, attr_dict=metadata)

