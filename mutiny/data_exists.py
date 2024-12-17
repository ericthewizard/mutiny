
import numpy as np
import mutiny

def data_exists(tvar):
    """
    Checks if a tplot variable exists

    Parameters
    ----------
    tvar: str
        Name of tplot variable to check

    Returns
    --------
    bool
        Retrun True if tplot variable exists.

    Example
    ----------
        >>> import mutiny
        >>> mutiny.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> mutiny.data_exists('a')

    """
    if tvar in mutiny.data_quants.keys():
        data = mutiny.get_data(tvar, dt=True)
        # multi-dimensional data returns a tuple, NRV variables return an ndarray
        if isinstance(data, tuple) or isinstance(data, np.ndarray) or isinstance(data, str) or isinstance(data, list):
            return True
    return False
