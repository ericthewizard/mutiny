import logging
import mutiny
import numpy as np
from mutiny import tplot_utilities as utilities


def options(name, option=None, value=None, opt_dict=None):
    """ Set a large variety of options for individual plots.

    Parameters
    ----------
        name : str
            Name or number of the tplot variable.
        option : str, optional
            The name of the option. See the options section below.
        value : str, int, float, list, optional
            The value of the option. See the options section below.
        opt_dict : dict, optional
            This can be a dictionary of option-value pairs. 'option' and 'value'
            will not be needed if this dictionary item is supplied.

    Options
    -------
        ======================  ===========  ===============================================================================
        Options                 Value type   Notes
        ======================  ===========  ===============================================================================
        Color                   str/list     red, green, blue, etc. Also takes in RGB tuples, i.e. (0,255,0) for green
        Colormap                str/list     https://matplotlib.org/examples/color/colormaps_reference.html.
        Spec                    int          1 sets the Tplot Variable to spectrogram mode, 0 reverts.
        Alt                     int          1 sets the Tplot Variable to altitude plot mode, 0 reverts.
        Map                     int          1 sets the Tplot Variable to latitude/longitude mode, 0 reverts.
        link                    list         Allows a user to reference one tplot variable to another.
        ylog                    int          1 sets the y axis to log scale, 0 reverts.
        zlog                    int          1 sets the z axis to log scale, 0 reverts (spectrograms only).
        legend_names            list         A list of strings that will be used to identify the lines.
        xlog_slice              bool         Sets x axis on slice plot to log scale if True.
        ylog                    bool         Set y axis on main plot window to log scale if True.
        ylog_slice              bool         Sets y axis on slice plot to log scale if True.
        zlog                    bool         Sets z axis on main plot window to log scale if True.
        line_style              str          scatter (to make scatter plots), or solid_line, dot, dash, dash_dot, dash_dot_dot_dot, long_dash.
        char_size               int          Defines character size for plot labels, etc.
        name                    str          The title of the plot.
        panel_size              flt          Number between (0,1], representing the percent size of the plot.
        basemap                 str          Full path and name of a background image for "Map" plots.
        alpha                   flt          Number between [0,1], gives the transparency of the plot lines.
        thick                   flt          Sets plot line width.
        yrange                  flt/list     Two numbers that give the y axis range of the plot.
        zrange                  flt/list     Two numbers that give the z axis range of the plot.
        xrange_slice            flt/list     Two numbers that give the x axis range of spectrogram slicing plots.
        yrange_slice            flt/list     Two numbers that give the y axis range of spectrogram slicing plots.
        ytitle                  str          Title shown on the y axis. Use backslash for new lines.
        ztitle                  str          Title shown on the z axis. Spec plots only. Use backslash for new lines.
        ysubtitle               str          Subtitle shown on the y axis.
        zsubtitle               str          Subtitle shown on the z axis. Spec plots only.
        plotter                 str          Allows a user to implement their own plotting script in place of the ones herein.
        crosshair_x             str          Title for x-axis crosshair.
        crosshair_y             str          Title for y-axis crosshair.
        crosshair_z             str          Title for z-axis crosshair.
        static                  str          Datetime string that gives desired time to plot y and z values from a spec plot.
        static_tavg             str          Datetime string that gives desired time-averaged y and z values to plot from a spec plot.
        t_average               int          Seconds around which the cursor is averaged when hovering over spectrogram plots.
        spec_plot_dim           int/str      If variable has more than two dimensions, this sets which dimension the "v"
        (cont)                  (cont)       variable will display on the y axis in spectrogram plots.
        (cont)                  (cont)       All other dimensions are summed into this one, unless "spec_slices_to_use"
        (cont)                  (cont)       is also set for this variable.
        spec_dim_to_plot        int/str      Same as spec_plot_dim, just with a slightly more descriptive name.
        spec_slices_to_use      str          Must be a dictionary of coordinate:values. If a variable has more than two
        (cont)                  (cont)       dimensions, spectrogram plots will plot values at that particular slice of
        (cont)                  (cont)       that dimension. See examples for how it works.
        border                  bool         Turns on or off the top/right axes that would create a box around the plot.
        var_label_ticks         int          Sets the number of ticks if this variable is displayed as an alternative x axis.
        data_gap                numerical    If there is a gap in the data larger than this number in seconds, then insert
        (cont)                  (cont)       NaNs. This is similar to using the degap procedure on the variable, but is
        (cont)                  (cont)       applied at plot-time, and does not persist in the variable data.
        y_major_ticks           list         A list of values that will be used to set the major ticks on the y axis.
        y_minor_tick_interval   numerical    The interval between minor ticks on the y axis.
        ======================  ===========  ===============================================================================


    Returns
    -------
        None

    Examples
    --------
        >>> # Change the y range of Variable1
        >>> import mutiny
        >>> x_data = [1,2,3,4,5]
        >>> y_data = [1,2,3,4,5]
        >>> mutiny.store_data("Variable1", data={'x':x_data, 'y':y_data})
        >>> mutiny.options('Variable1', 'yrange', [2,4])

        >>> # Change Variable1 to use a log scale
        >>> mutiny.options('Variable1', 'ylog', 1)
        >>> mutiny.tplot('Variable1')

        >>> # Multi-dimensional variable
        >>> y_data = np.random.rand(5, 4, 3)
        >>> v1_data = [0, 1, 3, 4]
        >>> v2_data = [1, 2, 3]
        >>> mutiny.store_data("Variable2", data={'x': x_data, 'y': y_data, 'v1': v1_data, 'v2': v2_data})
        >>> # Set the spectrogram plots to show dimension 'v2' at slice 'v1' = 0
        >>> mutiny.options('Variable2', 'spec', 1)
        >>> mutiny.options("Variable2", "spec_dim_to_plot", 'v2')
        >>> mutiny.options("Variable2", "spec_slices_to_use", {'v1': 0})
        >>> mutiny.tplot('Variable2')

    """

    if isinstance(name, int):
        name = list(mutiny.data_quants.keys())[name]

    if opt_dict is None:
        opt_dict = {option: value}
    else:
        if not isinstance(opt_dict,dict):
            logging.error("dict must be a dictionary object.  Returning.")
            return

    if not isinstance(name, list):
        name = [name]

    for i in name:

        for option, value in opt_dict.items():

            # Lower case option for consistency
            option = option.lower()

            if i not in mutiny.data_quants.keys():
                logging.info(str(i) + " is currently not in mutiny.")
                return

            if option == 'color':
                if isinstance(value, list):
                    mutiny.data_quants[i].attrs['plot_options']['extras']['line_color'] = value
                else:
                    mutiny.data_quants[i].attrs['plot_options']['extras']['line_color'] = [value]

            if option == 'link':
                if isinstance(value, list):
                    mutiny.link(i, value[1], value[0])

            if option == 'colormap':
                if isinstance(value, list):
                    mutiny.data_quants[i].attrs['plot_options']['extras']['colormap'] = value
                else:
                    mutiny.data_quants[i].attrs['plot_options']['extras']['colormap'] = [value]

            if option == 'colormap_width':
                mutiny.data_quants[i].attrs['plot_options']['extras']['colormap_width'] = value

            if option == 'second_axis_size':
                mutiny.data_quants[i].attrs['plot_options']['extras']['second_axis_size'] = value

            if option == 'spec':
                _reset_plots(i)
                if value:
                    if 'spec_bins' not in mutiny.data_quants[i].coords:
                        logging.warning(f"{i} does not contain coordinates for spectrogram plotting.  Continuing...")
                        continue
                    else:
                        mutiny.data_quants[i].attrs['plot_options']['extras']['spec'] = value
                        mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(mutiny.data_quants[i])

                else:
                    mutiny.data_quants[i].attrs['plot_options']['extras']['spec'] = value
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(mutiny.data_quants[i])

                # Set the default dimension to plot by.  All others will be summed over.
                if 'spec_dim_to_plot' not in mutiny.data_quants[i].attrs['plot_options']['extras']:
                    if 'v' in mutiny.data_quants[i].coords:
                        mutiny.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = 'v'
                    elif 'v2' in mutiny.data_quants[i].coords:
                        mutiny.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = 'v2'
                    else:
                        mutiny.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = 'v1'

            if option == 'alt':
                _reset_plots(i)
                mutiny.data_quants[i].attrs['plot_options']['extras']['alt'] = value

            if option == 'map':
                _reset_plots(i)
                mutiny.data_quants[i].attrs['plot_options']['extras']['map'] = value

            if option == 'legend_names' or option == 'labels':
                if isinstance(value, list):
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_names'] = value
                else:
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_names'] = [value]

            if option == 'legend_location' or option == 'labels_location':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_location'] = value

            if option == 'legend_size' or option == 'labels_size':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_size'] = value

            if option == 'legend_shadow' or option == 'labels_shadow':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_shadow'] = value

            if option == 'legend_title' or option == 'labels_title':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_title'] = value

            if option == 'legend_titlesize' or option == 'labels_titlesize':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_titlesize'] = value

            if option == 'legend_color' or option == 'labels_color':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_color'] = value

            if option == 'legend_edgecolor' or option == 'labels_edgecolor':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_edgecolor'] = value

            if option == 'legend_facecolor' or option == 'labels_facecolor':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_facecolor'] = value

            if option == 'legend_markerfirst' or option == 'labels_markerfirst':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_markerfirst'] = value

            if option == 'legend_markerscale' or option == 'labels_markerscale':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_markerscale'] = value

            if option == 'legend_markersize' or option == 'legend_markersize':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_markersize'] = value

            if option == 'legend_frameon' or option == 'labels_frameon':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_markerscale'] = value

            if option == 'legend_ncols' or option == 'labels_ncols':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['legend_ncols'] = value

            if option == 'xlog_slice':
                if value:
                    mutiny.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_axis_type'] = 'log'
                else:
                    mutiny.data_quants[i].attrs['plot_options']['slice_xaxis_opt']['xi_axis_type'] = 'linear'

            if option == 'ylog':
                negflag = 0 # _ylog_check(data_quants, value, i)
                if negflag == 0 and value:
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'log'
                else:
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_axis_type'] = 'linear'

            if option == 'ylog_slice':
                if value:
                    mutiny.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_axis_type'] = 'log'
                else:
                    mutiny.data_quants[i].attrs['plot_options']['slice_yaxis_opt']['yi_axis_type'] = 'linear'

            if option == 'zlog':
                # check for negative values and warn the user that they will be ignored
                negflag = _zlog_check(mutiny.data_quants, value, i)
                if negflag != 0 and value:
                    logging.warning(str(i) + ' contains negative values; setting the z-axis to log scale will cause the negative values to be ignored on figures.')

                if value:
                    mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'log'
                else:
                    mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['z_axis_type'] = 'linear'

            if option == 'nodata':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['visible'] = value

            # Obsolete? (except for value='none'?) JWL 2024-03-21
            # These don't seem to be the correct format for matplotlib parameterized line styles.
            if option == 'line_style' or option == 'linestyle':
                if value == 0 or value == 'solid_line':
                    to_be = []
                elif value == 1 or value == 'dot':
                    to_be = [2, 4]
                elif value == 2 or value == 'dash':
                    to_be = [6]
                elif value == 3 or value == 'dash_dot':
                    to_be = [6, 4, 2, 4]
                elif value == 4 or value == 'dash_dot_dot_dot':
                    to_be = [6, 4, 2, 4, 2, 4, 2, 4]
                elif value == 5 or value == 'long_dash':
                    to_be = [10]
                else:
                    to_be=value

                # This does not appear to be used by tplot. JWL 2024-03-21
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['line_style'] = to_be

                mutiny.data_quants[i].attrs['plot_options']['line_opt']['line_style_name'] = _convert_to_matplotlib_linestyle(value)

                if(value == 6 or value == 'none'):
                    mutiny.data_quants[i].attrs['plot_options']['line_opt']['visible'] = False

            if option == 'char_size' or option == 'charsize':
                mutiny.data_quants[i].attrs['plot_options']['extras']['char_size'] = value

            if option == 'name':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['name'] = value

            if option == 'title':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['title'] = value

            if option == "panel_size":
                if value > 1 or value <= 0:
                    logging.info("Invalid panel_size value (%f). Should be in (0, 1]",value)
                    return
                mutiny.data_quants[i].attrs['plot_options']['extras']['panel_size'] = value

            if option == 'basemap':
                mutiny.data_quants[i].attrs['plot_options']['extras']['basemap'] = value

            if option == 'alpha':
                if value > 1 or value < 0:
                    logging.info("Invalid alpha value (%f). Should be [0, 1]",value)
                    return
                mutiny.data_quants[i].attrs['plot_options']['extras']['alpha'] = value

            if option == 'marker':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['marker'] = value

            if option == 'errorevery':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['errorevery'] = value

            if option == 'capsize':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['capsize'] = value

            if option == 'ecolor':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['ecolor'] = value

            if option == 'elinewidth':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['elinewidth'] = value

            if option == 'marker_size':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['marker_size'] = value

            if option == 'markevery':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['markevery'] = value

            if option == 'symbols':
                mutiny.data_quants[i].attrs['plot_options']['line_opt']['symbols'] = value

            if option == 'xtick_length':
                mutiny.data_quants[i].attrs['plot_options']['extras']['xtick_length'] = value

            if option == 'ytick_length':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ytick_length'] = value

            if option == 'xtick_width':
                mutiny.data_quants[i].attrs['plot_options']['extras']['xtick_width'] = value

            if option == 'ytick_width':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ytick_width'] = value

            if option == 'xtick_color':
                mutiny.data_quants[i].attrs['plot_options']['extras']['xtickcolor'] = value

            if option == 'ytick_color':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ytickcolor'] = value

            if option == 'xtick_labelcolor':
                mutiny.data_quants[i].attrs['plot_options']['extras']['xtick_labelcolor'] = value

            if option == 'ytick_labelcolor':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ytick_labelcolor'] = value

            if option == 'xtick_direction':
                mutiny.data_quants[i].attrs['plot_options']['extras']['xtick_direction'] = value

            if option == 'ytick_direction':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ytick_direction'] = value

            if option == 'right_axis':
                mutiny.data_quants[i].attrs['plot_options']['extras']['right_axis'] = value

            if option == 'thick':
                if isinstance(value, list):
                    mutiny.data_quants[i].attrs['plot_options']['line_opt']['line_width'] = value
                else:
                    mutiny.data_quants[i].attrs['plot_options']['line_opt']['line_width'] = [value]

            if option == 'yrange' or option == 'y_range':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = [value[0], value[1]]
                # track whether the yrange option was set by the user
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range_user'] = True

            if option == 'y_major_ticks':
                # check whether the value is 1D array-like
                if isinstance(value, (list, np.ndarray)):
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_major_ticks'] = value
                else:
                    logging.warning('y_major_ticks must be a 1D array-like object')

            if option == 'y_minor_tick_interval':
                # check whether the value is a number
                if isinstance(value, (int, float)):
                    mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_minor_tick_interval'] = value
                else:
                    logging.warning('y_minor_tick_interval must be a number')

            if option == 'zrange' or option == 'z_range':
                mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['z_range'] = [value[0], value[1]]

            if option == 'xrange_slice':
                plt_opts = mutiny.data_quants[i].attrs['plot_options']
                if plt_opts.get('slice_xaxis_opt') is not None:
                    plt_opts['slice_xaxis_opt']['xi_range'] = [value[0], value[1]]

            if option == 'yrange_slice':
                plt_opts = mutiny.data_quants[i].attrs['plot_options']
                if plt_opts.get('slice_yaxis_opt') is not None:
                    plt_opts['slice_yaxis_opt']['yi_range'] = [value[0], value[1]]

            if option == 'xtitle':
                mutiny.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_label'] = value

            if option == 'ytitle':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_label'] = value

            if option == 'ztitle':
                mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_label'] = value

            if option == 'xsubtitle':
                mutiny.data_quants[i].attrs['plot_options']['xaxis_opt']['axis_subtitle'] = value

            if option == 'ysubtitle':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_subtitle'] = value

            if option == 'zsubtitle':
                mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_subtitle'] = value

            if option == 'ytitle_color':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['axis_color'] = value

            if option == 'ztitle_color':
                mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['axis_color'] = value

            if option == 'ybar':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ybar'] = value

            if option == 'ybar_color':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ybar'] = value

            if option == 'ybar_size':
                mutiny.data_quants[i].attrs['plot_options']['extras']['ysize'] = value

            if option == 'plotter':
                _reset_plots(i)
                mutiny.data_quants[i].attrs['plot_options']['extras']['plotter'] = value

            if option == 'crosshair_x':
                mutiny.data_quants[i].attrs['plot_options']['xaxis_opt']['crosshair'] = value

            if option == 'crosshair_y':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['crosshair'] = value

            if option == 'crosshair_z':
                mutiny.data_quants[i].attrs['plot_options']['zaxis_opt']['crosshair'] = value

            if option == 'static':
                mutiny.data_quants[i].attrs['plot_options']['extras']['static'] = value

            if option == 'static_tavg':
                mutiny.data_quants[i].attrs['plot_options']['extras']['static_tavg'] = [value[0], value[1]]

            if option == 't_average':
                mutiny.data_quants[i].attrs['plot_options']['extras']['t_average'] = value

            if option == 'data_gap': #jmm, 2023-06-20
                mutiny.data_quants[i].attrs['plot_options']['extras']['data_gap'] = value

            if option == 'spec_dim_to_plot' or option == 'spec_plot_dim':
                if len(mutiny.data_quants[i].values.shape) <= 2:
                    logging.warning(f"Must have more than 2 coordinate dimensions to set spec_coord_to_plot for {mutiny.data_quants[i].name}")
                    continue

                # Set the 'spec_dim_to_plot' value to either 'v' or 'v1', 'v2', 'v3', etc.
                if isinstance(value, int):
                    coord_to_plot = "v" + str(value)
                    if coord_to_plot not in mutiny.data_quants[i].coords:
                        if value == 1:
                            coord_to_plot = "v"
                            if coord_to_plot not in mutiny.data_quants[i].coords:
                                logging.warning(f"Dimension {value} not found in {mutiny.data_quants[i].name}")
                                continue
                        else:
                            logging.warning(f"Dimension {value} not found in {mutiny.data_quants[i].name}")
                            continue
                    mutiny.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = coord_to_plot
                elif isinstance(value, str):
                    coord_to_plot = value
                    if coord_to_plot not in mutiny.data_quants[i].coords:
                        logging.warning(f"Dimension {value} not found in {mutiny.data_quants[i].name}")
                        continue
                    else:
                        mutiny.data_quants[i].attrs['plot_options']['extras']['spec_dim_to_plot'] = value

                # If we're plotting against different coordinates, we need to change what we consider the "spec_bins"
                mutiny.data_quants[i].coords['spec_bins'] = mutiny.data_quants[i].coords[coord_to_plot]
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_range'] = utilities.get_y_range(mutiny.data_quants[i])

            if option == 'spec_slices_to_use':
                if not isinstance(value, dict):
                    logging.error("Must be a dictionary object in the format {'v2':15, 'v3':7}")
                    return
                else:
                    for coord in value:
                        if coord not in mutiny.data_quants[i].coords:
                            logging.warning(f"Dimension {coord} not found in {mutiny.data_quants[i].name}")
                            continue

                mutiny.data_quants[i].attrs['plot_options']['extras']['spec_slices_to_use'] = value

            if option == 'border':
                mutiny.data_quants[i].attrs['plot_options']['extras']['border'] = value

            if option == 'var_label_ticks':
                mutiny.data_quants[i].attrs['plot_options']['var_label_ticks'] = value

            if option == 'y_interp':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_interp'] = value

            if option == 'y_interp_points':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_interp_points'] = value

            if option == 'x_interp':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['x_interp'] = value

            if option == 'x_interp_points':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['x_interp_points'] = value
            if option == 'y_no_resample':
                mutiny.data_quants[i].attrs['plot_options']['yaxis_opt']['y_no_resample'] = value
    return


def _ylog_check(data_quants, value, i):
    negflag = 0
    namedata = data_quants[i]
    # check variable data
    # if negative numbers, don't allow log setting
    datasets = [namedata]
    for oplot_name in namedata.attrs['plot_options']['overplots']:
        datasets.append(data_quants[oplot_name])

    if value == 1:
        for dataset in datasets:
            if 'spec' not in dataset.attrs['plot_options']['extras']:
                if dataset.min(skipna=True) < 0:
                    logging.warning('Negative data is incompatible with log plotting.')
                    negflag = 1
                    break
            else:
                if dataset.attrs['plot_options']['extras']['spec'] == 1:
                    if dataset.coords['spec_bins'].min(skipna=True) < 0:
                        logging.warning('Negative data is incompatible with log plotting.')
                        negflag = 1
                        break
    elif value != 1:
        # Using the 'negflag' as a way to not log something if the user doesn't want it to be logged
        negflag = 1
    return negflag


def _zlog_check(data_quants, value, i):
    negflag = 0
    namedata = data_quants[i]
    # check variable data
    # if negative numbers, don't allow log setting
    datasets = [namedata]
    for oplot_name in namedata.attrs['plot_options']['overplots']:
        datasets.append(data_quants[oplot_name])

    for dataset in datasets:
        if value == 1:
            if 'spec' in dataset.attrs['plot_options']['extras']:
                if dataset.attrs['plot_options']['extras']['spec'] == 1:
                    if dataset.min(skipna=True) < 0:
                        negflag = 1
                        break
        elif value != 1:
            # Using the 'negflag' as a way to not log something if the user doesn't want it to be logged
            negflag = 1
    return negflag


def _reset_plots(name):
    if isinstance(mutiny.data_quants[name], dict):  # non-record varying variable
        return
    mutiny.data_quants[name].attrs['plot_options']['extras']['spec'] = 0
    mutiny.data_quants[name].attrs['plot_options']['extras']['alt'] = 0
    mutiny.data_quants[name].attrs['plot_options']['extras']['map'] = 0
    mutiny.data_quants[name].attrs['plot_options']['extras']['plotter'] = None

def _convert_to_matplotlib_linestyle(linestyle):
    if not isinstance(linestyle,list):
        linestyle = [linestyle]
    converted_linestyles = []
    for ls in linestyle:
        if ls == 'solid_line':
            converted_linestyles.append('solid')
        elif ls == 'dot':
            converted_linestyles.append('dotted')
        elif ls == 'dash':
            converted_linestyles.append('dashed')
        elif ls == 'dash_dot':
            converted_linestyles.append('dashdot')
        else:
            converted_linestyles.append(ls)
    return converted_linestyles


