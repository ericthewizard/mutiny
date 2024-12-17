# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
import logging


def get_ylimits(name, trg=None):
    """
    Extracts the y-limits from the Tplot Variables stored in memory.

    Parameters
    ----------
    name : str
        Name of the tplot variable.
    trg : list, optional
        The time range to look in.

    Returns
    -------
    ymin : int, float, numeric type of mutiny data
        The minimum value of y.
    ymax : int, float, numeric type of mutiny data
        The maximum value of y.

    Examples
    --------
    >>> import mutiny
    >>> x_data = [1, 2, 3, 4, 5]
    >>> y_data = [1, 2, 3, 4, 5]
    >>> mutiny.store_data("Variable1", data={'x': x_data, 'y': y_data})
    >>> y1, y2 = mutiny.get_ylimits("Variable1")
    """

    if isinstance(name, int):
        name = list(mutiny.data_quants.keys())[name-1]
    if not isinstance(name, list):
        name = [name]
    name_num = len(name)
    ymin = None
    ymax = None

    for i in range(name_num):

        if name[i] not in mutiny.data_quants.keys():
            logging.info(str(name[i]) + " is currently not in mutiny.")
            return
        y = mutiny.data_quants[name[i]]

        # Slice the data around a time range
        if trg is not None:
            y = y.sel(time=slice(trg[0], trg[1]))

        ymin = y.min(skipna=True).values.item()
        ymax = y.max(skipna=False).values.item()

    return ymin, ymax
