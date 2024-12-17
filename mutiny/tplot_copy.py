# Copyright 2020 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import logging
import mutiny
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
        >>> import mutiny
        >>> mutiny.tplot_copy("Variable1", "Variable2")

    """

    # if old name input is a number, convert to corresponding name
    if isinstance(old_name, int):
        if isinstance(mutiny.data_quants[old_name], dict):
            old_name = mutiny.data_quants[old_name]['name']
        else:
            old_name = mutiny.data_quants[old_name].name

    # check if old name is in current dictionary
    if old_name not in mutiny.data_quants.keys():
        logging.info("The name %s is currently not in mutiny",old_name)
        return

    # Add a new data quantity with the copied data
    if isinstance(mutiny.data_quants[old_name], dict):
        # old variable is a non-record varying variable
        mutiny.store_data(new_name, data={'y': mutiny.data_quants[old_name]['data']})
    else:
        mutiny.data_quants[new_name] = deepcopy(mutiny.data_quants[old_name])
        mutiny.data_quants[new_name].name = new_name

    return
