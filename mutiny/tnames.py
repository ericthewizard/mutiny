import re
import logging
from mutiny import tplot_names
from .wildcard_routines import wildcard_expand


def tnames(pattern=None, regex=None):
    """
    Find tplot names matching a wildcard pattern.

    Parameters
    ----------
    pattern : str or list of str, optional
        Pattern(s) to search for.
        It can be a string or a list of strings (multiple patterns).
        Each pattern can contain wildcards such as * and ?, using unix-style matching.
        The default is None
    regex : str, optional
        Regular expression pattern to search for.
        If regex is provided, the pattern argument is ignored.
        The default is None.
        If both pattern and regex are None, all tplot names are returned.

    Returns
    -------
    name_list : list of str
        List of tplot variables.

    Examples
    -------
        >>> import mutiny
        >>> from pyspedas.themis import fgm
        >>> fgm(trange=['2007-03-23','2007-03-24'], probe='a')
        >>> mutiny.tnames('tha_fgs*')
        >>> mutiny.tnames('th?_fgs_gsm')
    """
    name_list = list()
    all_names = tplot_names(quiet=True)

    if len(all_names) < 1:
        # No tplot variables found
        pass
    elif pattern is None and regex is None:
        name_list.extend(all_names)
    elif regex is not None:
        # Use re to find all names that match the regular expression
        try:
            # Check if regex is a valid regular expression
            re.compile(regex)

            for p in all_names:
                if re.match(regex, p):
                    name_list.append(p)
        except re.error:
            logging.error("Invalid regular expression.")
    elif pattern is not None:
        name_list = wildcard_expand(all_names,pattern)

    return name_list
