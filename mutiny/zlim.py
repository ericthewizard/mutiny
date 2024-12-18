# Copyright 2018 Regents of the University of Colorado. All Rights Reserved.
# Released under the MIT license.
# This software was developed at the University of Colorado's Laboratory for Atmospheric and Space Physics.
# Verify current version before use at: https://github.com/MAVENSDC/mutiny

import mutiny
import logging

def zlim(name, min, max):
    """
    This function will set the z axis range displayed for a specific tplot variable.
    This is only used for spec plots, where the z axis represents the magnitude of the values
    in each bin.  
    
    Parameters
    ----------
        name : str
            The name of the tplot variable that you wish to set z limits for.  
        min : flt
            The start of the z axis.
        max : flt
            The end of the z axis.   
            
    Returns
    -------
        None
    
    Examples
    --------
        >>> # Change the z range of Variable1 
        >>> import mutiny
        >>> x_data = [1,2,3]
        >>> y_data = [ [1,2,3] , [4,5,6], [7,8,9] ]
        >>> v_data = [1,2,3]
        >>> mutiny.store_data("Variable3", data={'x':x_data, 'y':y_data, 'v':v_data})
        >>> mutiny.zlim('Variable1', 2, 3)

    """
    if name not in mutiny.data_quants.keys():
        logging.info("The name %s is currently not in mutiny.", name)
        return

    mutiny.options(name,'z_range',[min,max])
    return