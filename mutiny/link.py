# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import logging
import mutiny
import numpy as np

def link(names, link_name, link_type='alt'):
    '''
    Simply adds metadata to the tplot variables, specifying which other tplot variables
    contain other coordinates, typically positional information.

    Parameters:
        names: str or list of str
            The names to link
        link_name: str
            The tplot variable to link to the names
        link_type: str
            The relationship that link_name has to the names.  Values can be
            lat, lon, alt, x, y, z, mso_x, mso_y, mso_z
    '''

    link_type = link_type.lower()
    if not isinstance(names, list):
        names = [names]
        
    for i in names:
        if i not in mutiny.data_quants.keys():
            logging.info(str(i) + " is not currently in mutiny.")
            return
        
        if isinstance(i,int):
            i = list(mutiny.data_quants.keys())[i-1]

        if isinstance(mutiny.data_quants[i], dict):  # non-record varying variable
            continue
        mutiny.data_quants[mutiny.data_quants[i].name].attrs['plot_options']['links'][link_type] = link_name
                
    return



