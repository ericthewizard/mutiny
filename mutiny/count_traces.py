
import numpy as np
import mutiny
import logging

def count_traces(tvar):
    """
    Count the total number of line traces in a variable or list of variables

    Parameters
    ----------
    tvar: str or list of str
        tplot variables with traces to be counted

    Returns
    -------
    int
        Number of traces found in the input variables.  Spectrograms are not counted.

    Examples
    --------
        >>> import mutiny
        >>> mutiny.store_data('a', data={'x': range(10), 'y': range(10)})
        >>> mutiny.store_data('b', data={'x': range(10), 'y': range(10)})
        >>> mutiny.store_data('pseudovar', data=['a','b'])
        >>> mutiny.count_traces('a')  # 1
        >>> mutiny.count_traces('pseudovar') # 2

    """
    trace_count = 0
    if not isinstance(tvar,list):
        tvar = [tvar]
    for v in tvar:
        if v in mutiny.data_quants.keys():
            data=mutiny.get_data(v, dt=True)

            if mutiny.is_pseudovariable(v):
                components = mutiny.data_quants[v].attrs['plot_options']['overplots_mpl']
                trace_count += count_traces(components)
            else:
                plot_extras = mutiny.data_quants[v].attrs['plot_options']['extras']
                if plot_extras.get('spec') is not None:
                    spec = plot_extras['spec']
                else:
                    spec = False

                if len(data.y.shape) == 1:
                    num_lines = 1
                else:
                    num_lines = data.y.shape[1]

                if not spec:
                    trace_count += num_lines
        else:
            logging.warning('The name %s is not in mutiny',v)
    return trace_count
