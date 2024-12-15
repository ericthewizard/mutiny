# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutinyplot

import mutinyplot
import fnmatch
import logging


def del_data(name=None):
    """
    This function will delete tplot variables that are already stored in memory.  
    
    Parameters
    ----------
        name : str, optional 
            Name of the tplot variable to be deleted.  If no name is provided, then 
            all tplot variables will be deleted.  
         
    Returns
    -------
        None
        
    Examples
    --------
        >>> # Delete Variable 1
        >>> import mutinyplot
        >>> mutinyplot.del_data("Variable1")

    """
    if name is None:
        tplot_names = list(mutinyplot.data_quants.keys())
        for i in tplot_names:
            del mutinyplot.data_quants[i]
        return
    
    if not isinstance(name, list):
        name = [name]
    
    entries = []
    for i in name:
        if ('?' in i) or ('*' in i):
            for j in mutinyplot.data_quants.keys():
                if isinstance(mutinyplot.data_quants[j], dict):
                    # NRV variable
                    var_verif = fnmatch.fnmatch(mutinyplot.data_quants[j]['name'], i)
                    if var_verif == 1:
                        entries.append(mutinyplot.data_quants[j]['name'])
                    else:
                        continue
                else:
                    var_verif = fnmatch.fnmatch(mutinyplot.data_quants[j].name, i)
                    if var_verif == 1:
                        entries.append(mutinyplot.data_quants[j].name)
                    else:
                        continue
            for key in entries:
                if key in mutinyplot.data_quants:
                    del mutinyplot.data_quants[key]
        elif i not in mutinyplot.data_quants.keys():
            logging.info(str(i) + " is currently not in mutinyplot.")
            return
        
        else:
            if isinstance(mutinyplot.data_quants[i], dict):
                temp_data_quants = mutinyplot.data_quants[i]
                str_name = temp_data_quants['name']
            else:
                temp_data_quants = mutinyplot.data_quants[i]
                str_name = temp_data_quants.name
            
            del mutinyplot.data_quants[str_name]
        
    return