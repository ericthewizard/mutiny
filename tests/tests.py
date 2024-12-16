import numpy as np
import mutinyplot
from mutinyplot import store, tplot, options
from mutinyplot import get_data, store_data, options, tplot_options, tlimit, timebar
import os

current_directory = os.path.dirname(os.path.realpath(__file__)) + os.path.sep


def test_simple():
    store_data('simple', data={'x': [1, 2, 3, 4, 5], 'y': [1, 5, 1, 5, 1]})
    tplot_options('title', 'simple')
    tplot('simple', display=False, save_png=current_directory + 'simple')


def test_symbols():
    store_data('symbols', data={'x': [1, 2, 3, 4, 5], 'y': [1, 5, 1, 5, 1]})
    options('symbols', 'symbols', True)
    tplot_options('title', 'symbols')
    tplot('symbols', display=False, save_png=current_directory + 'symbols')


def test_markers():
    store_data('markers', data={'x': [1, 2, 3, 4, 5], 'y': [1, 5, 6, 5, 1]})
    options('markers', 'marker', 'v')
    tplot_options('title', 'markers')
    tplot('markers', display=False, save_png=current_directory + 'markers')

    options('markers', 'marker_size', 100)
    tplot_options('title', 'marker_size')
    tplot('markers', display=False, save_png=current_directory + 'marker_size')


def test_margins():
    store_data('margins', data={'x': [1, 2, 3, 4, 5], 'y': [1, 5, 1, 5, 1]})
    tplot_options('title', 'margins')
    tplot_options('xmargin', [0.2, 0.2])
    tplot_options('ymargin', [0.2, 0.2])
    tplot('margins', display=False, save_png=current_directory + 'margins')
    tplot_options('xmargin', None)
    tplot_options('ymargin', None)


def test_pseudo_vars():
    store_data('var1', data={'x': [1, 2, 3, 4, 5], 'y': [3, 3, 3, 3, 3]})
    store_data('var2', data={'x': [1, 2, 3, 4, 5], 'y': [7, 7, 7, 7, 7]})
    store_data('var_combined', data=['var1', 'var2'])
    options('var_combined', 'yrange', [1, 10])
    options('var_combined', 'color', ['red', 'blue'])
    options('var_combined', 'legend_names', ['red', 'blue'])
    options('var_combined', 'thick', [2, 4])
    options('var_combined', 'linestyle', ['dotted', 'dashed'])
    options('var_combined', 'legend_names', ['red', 'blue'])
    options('var_combined', 'ytitle', 'This is a pseudo-variable')
    tplot_options('title', 'pseudo_vars')
    tplot('var_combined', display=False, save_png=current_directory + 'pseudo_vars')


def test_pseudo_var_spectra():
    data = np.array([[0, 1, 2, 3, 4],
                     [5, 6, 7, 8, 9],
                     [10, 11, 12, 13, 14],
                     [15, 16, 17, 18, 19],
                     [20, 21, 22, 23, 24]])

    store_data('bins_1', data={'x': [1, 2, 3, 4, 5], 'y': data.transpose(), 'v': [10, 20, 30, 40, 50]})
    store_data('bins_2', data={'x': [1, 2, 3, 4, 5], 'y': data.transpose() + 25.0, 'v': [100, 120, 130, 140, 150]})

    options('bins_1', 'spec', 1)
    options('bins_1', 'yrange', [0, 200])
    options('bins_1', 'Colormap', 'spedas')
    options('bins_2', 'spec', 1)
    options('bins_2', 'yrange', [0, 200])
    options('bins_2', 'Colormap', 'spedas')

    store_data('combined_spec', data=['bins_1', 'bins_2'])
    options('combined_spec', 'yrange', [0, 200])

    tplot_options('xmargin', [0.2, 0.2])
    tplot_options('title', 'pseudo_var_spectra')
    tplot('combined_spec', display=False, save_png=current_directory + 'combined_spec')


def test_pseudo_var_spectra_zrange():
    data = np.array([[0, 1, 2, 3, 4],
                     [5, 6, 7, 8, 9],
                     [10, 11, 12, 13, 14],
                     [15, 16, 17, 18, 19],
                     [20, 21, 22, 23, 24]])

    store_data('bins_1', data={'x': [1, 2, 3, 4, 5], 'y': data.transpose(), 'v': [10, 20, 30, 40, 50]})
    store_data('bins_2', data={'x': [1, 2, 3, 4, 5], 'y': data.transpose() + 25.0, 'v': [100, 120, 130, 140, 150]})

    options('bins_1', 'spec', 1)
    options('bins_1', 'yrange', [0, 200])
    options('bins_1', 'Colormap', 'spedas')
    options('bins_1', 'zrange', [0, 50])
    options('bins_2', 'spec', 1)
    options('bins_2', 'yrange', [0, 200])
    options('bins_2', 'Colormap', 'spedas')
    options('bins_2', 'zrange', [0, 50])

    store_data('combined_spec', data=['bins_1', 'bins_2'])
    options('combined_spec', 'yrange', [0, 200])
    options('combined_spec', 'zrange', [0, 50])

    tplot_options('xmargin', [0.2, 0.2])
    tplot_options('title', 'combined_spec_zrange')
    tplot('combined_spec', display=False, save_png=current_directory + 'combined_spec_zrange')


def test_pseudo_var_options():
    store('region1', data={'x': [1, 2, 3, 4, 5, 6], 'y': [1, 1, 1, 1, 1, 1]})
    store('region2', data={'x': [1.5, 2.5, 3.5, 4.5, 5.5], 'y': [3, 3, 3, 3, 3]})
    store('region3', data={'x': [1, 2, 3, 4, 5, 6], 'y': [2, 2, 2, 2, 2, 2]})
    store('combined', data='region1 region2 region3')
    options('combined', 'marker', ['o', 'v', '<'])
    options('combined', 'marker_size', [2, 10, 20])
    tplot_options('title', 'pseudo variable combined markers')
    tplot('combined', display=False, save_png=current_directory + 'pseudo_markers')


def test_nans_log_scale():
    """
    regression test for a crash when the data are all NaNs, and zlog is set
    """
    tplot_options('title', 'NaNs zlog regression test - should be empty')
    y = np.zeros((5, 3))
    y[:] = np.nan
    store_data('test_spec_nan', data={'x': [1, 2, 3, 4, 5], 'y': y, 'v': [6, 7, 8]})
    options('test_spec_nan', 'spec', True)
    options('test_spec_nan', 'zlog', True)
    tplot('test_spec_nan', display=False, save_png=current_directory + 'nans_zlog_regression')