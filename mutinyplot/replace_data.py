import mutinyplot
import numpy as np
from mutinyplot import tplot_utilities as utilities
import logging


def replace_data(tplot_name, new_data):
    """
    This function will replace all of the data in a tplot variable.

    Parameters
    ----------
    tplot_name : str
        The name of the tplot variable.
    new_data : array_like
        The new data to replace the existing data.
        This can be any object that can be converted into an np.array.

    Returns
    -------
    None

    Examples
    --------
    >>> # Replace data into an existing variable
    >>> import mutinyplot
    >>> mutinyplot.store_data("v1", data={'x':[1,2,3,4],'y':[1,2,3,4]})
    >>> print(mutinyplot.get_data('v1'))
    >>> mutinyplot.replace_data("v1",[5,6,7,8])
    >>> print(mutinyplot.get_data('v1'))
    """

    # if old name input is a number, convert to corresponding name
    if isinstance(tplot_name, int):
        tplot_name = mutinyplot.data_quants[tplot_name].name

    # check if old name is in current dictionary
    if tplot_name not in mutinyplot.data_quants.keys():
        logging.info(f"{tplot_name} is currently not in mutinyplot")
        return

    new_data_np = np.asarray(new_data)
    shape_old = mutinyplot.data_quants[tplot_name].values.shape
    shape_new = new_data_np.shape
    if shape_old != shape_new:
        logging.info(
            f"Dimensions do not match for replace data. {shape_new} does not equal {shape_old}.  Returning..."
        )
        return

    mutinyplot.data_quants[tplot_name].values = new_data_np

    mutinyplot.data_quants[tplot_name].attrs["plot_options"]["yaxis_opt"]["y_range"] = (
        utilities.get_y_range(mutinyplot.data_quants[tplot_name])
    )

    return
