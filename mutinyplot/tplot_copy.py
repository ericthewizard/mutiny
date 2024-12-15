# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutinyplot

import logging
import mutinyplot
from copy import deepcopy
from collections import OrderedDict


def tplot_copy(old_name, new_name):
    """
    This function will copy a tplot variables that is already stored in memory.

    Parameters
    ----------
        name : str
            Old name of the Tplot Variable
        new_name : str
            Name of the copied Tplot Variable

    Returns
    -------
        None

    Examples
    --------
        >>> # Copy Variable 1 into a new Variable 2
        >>> import mutinyplot
        >>> mutinyplot.tplot_copy("Variable1", "Variable2")

    """

    # if old name input is a number, convert to corresponding name
    if isinstance(old_name, int):
        if isinstance(mutinyplot.data_quants[old_name], dict):
            old_name = mutinyplot.data_quants[old_name]['name']
        else:
            old_name = mutinyplot.data_quants[old_name].name

    # check if old name is in current dictionary
    if old_name not in mutinyplot.data_quants.keys():
        logging.info("The name %s is currently not in mutinyplot",old_name)
        return

    # Add a new data quantity with the copied data
    if isinstance(mutinyplot.data_quants[old_name], dict):
        # old variable is a non-record varying variable
        mutinyplot.store_data(new_name, data={'y': mutinyplot.data_quants[old_name]['data']})
    else:
        mutinyplot.data_quants[new_name] = deepcopy(mutinyplot.data_quants[old_name])
        mutinyplot.data_quants[new_name].name = new_name

    return
