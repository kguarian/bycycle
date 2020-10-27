"""Utility functions for working with ByCycle DataFrames."""

import numpy as np
import pandas as pd

from bycycle.utils.checks import check_param

###################################################################################################
###################################################################################################

def limit_df(df, fs, start=None, stop=None):
    """Restrict dataframe to be within time limits.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe output of :func:`~.compute_features`.
    fs : float
        Sampling rate, in Hz.
    start : float, optional
        The lower time limit, in seconds, to restrict the df.
    stop : float, optional
        The upper time limit, in seconds, to restrict the df.

    Returns
    -------
    df : pandas.DataFrame
        A limited dataframe of cycle features.

    Notes
    -----
    Cycles, or rows in the `df`, are included if any segment of the cycle falls after the
    `stop` time or before the `end` time.

    Examples
    --------
    Limit a samples dataframe to the first second of a simulated signal:

    >>> from neurodsp.sim import sim_bursty_oscillation
    >>> from bycycle.features import compute_features
    >>> fs = 500
    >>> sig = sim_bursty_oscillation(10, fs, freq=10)
    >>> df_features = compute_features(sig, fs, f_range=(8, 12))
    >>> df_features = limit_df(df_features, fs, start=0, stop=1)
    """

    # Ensure arguments are within valid range
    check_param(fs, 'fs', (0, np.inf))
    check_param(start, 'start', (0, stop))
    check_param(stop, 'stop', (start, np.inf))

    center_e, side_e = get_extrema_df(df)

    start = 0 if start is None else start

    df = df[df['sample_next_' + side_e].values >= start*fs]

    if stop is not None:
        df = df[df['sample_last_' + side_e].values < stop*fs]

    # Shift sample indices to start at 0
    df['sample_last_' + side_e] = df['sample_last_' + side_e] - int(fs * start)
    df['sample_next_' + side_e] = df['sample_next_' + side_e] - int(fs * start)
    df['sample_' + center_e] = df['sample_' + center_e] - int(fs * start)
    df['sample_zerox_rise'] = df['sample_zerox_rise'] - int(fs * start)
    df['sample_zerox_decay'] = df['sample_zerox_decay'] - int(fs * start)

    return df


def get_extrema_df(df):
    """Determine whether cycles are peak or trough centered.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe output of :func:`~.compute_features`.

    Returns
    -------
    center_e : str
        Center extrema, either 'peak' or 'trough'.
    side_e : str
        Side extrema, either 'peak' or 'trough'.

    Examples
    --------
    Confirm that cycles are peak-centered:

    >>> from neurodsp.sim import sim_bursty_oscillation
    >>> from bycycle.features import compute_features
    >>> fs = 500
    >>> sig = sim_bursty_oscillation(10, fs, freq=10)
    >>> df_features = compute_features(sig, fs, f_range=(8, 12), center_extrema='peak')
    >>> center_e, side_e = get_extrema_df(df_features)
    >>> center_e
    'peak'
    """

    center_e = 'peak' if 'sample_peak' in df.columns else 'trough'
    side_e = 'trough' if center_e == 'peak' else 'peak'

    return center_e, side_e


def rename_extrema_df(center_extrema, df_features, return_samples=True):
    """Rename a dataframe based on the centered extrema.

    Parameters
    ----------
    center_extrema : {'trough', 'peak'}
        Which extrema is centered.
    df_shape_features : pandas.DataFrames
        Bycycle dataframes to rename, given the centered extrema.
    return_samples : bool, optional, default: True
        Whether to rename sample columns if ``returns_samples`` is True when computing
        ``df_shape_features`` using :func:`~.compute_shape_features`.

    Returns
    -------
    df_features : pandas.DataFrames
        Updated dataframes.

    Examples
    --------
    Convert the column labels of a peak-centered dataframe to a trough-centered dataframe:

    >>> from neurodsp.sim import sim_bursty_oscillation
    >>> from bycycle.features import compute_features
    >>> fs = 500
    >>> sig = sim_bursty_oscillation(10, fs, freq=10)
    >>> sig = -sig  # invert the signal, flipping peaks and troughs
    >>> df_features = compute_features(sig, fs, f_range=(8, 12), center_extrema='peak')
    >>> df_features = rename_extrema_df('trough', df_features)
    """

    # Rename columns if they are actually trough-centered
    if center_extrema == 'trough':

        features_rename_dict = {'time_peak': 'time_trough',
                                'time_trough': 'time_peak',
                                'volt_peak': 'volt_trough',
                                'volt_trough': 'volt_peak',
                                'time_rise': 'time_decay',
                                'time_decay': 'time_rise',
                                'volt_rise': 'volt_decay',
                                'volt_decay': 'volt_rise'}

        df_features.rename(columns=features_rename_dict, inplace=True)

        # Need to reverse symmetry measures
        df_features['volt_peak'] = -df_features['volt_peak']
        df_features['volt_trough'] = -df_features['volt_trough']
        df_features['time_rdsym'] = 1 - df_features['time_rdsym']
        df_features['time_ptsym'] = 1 - df_features['time_ptsym']

        if return_samples:

            samples_rename_dict = {'sample_peak': 'sample_trough',
                                   'sample_zerox_decay': 'sample_zerox_rise',
                                   'sample_zerox_rise': 'sample_zerox_decay',
                                   'sample_last_zerox_decay': 'sample_last_zerox_rise',
                                   'sample_last_trough': 'sample_last_peak',
                                   'sample_next_trough': 'sample_next_peak'}

            df_features.rename(columns=samples_rename_dict, inplace=True)

    return df_features


def split_samples_df(df_features):
    """Move cyclepoints sample indices columns to a separate dataframe.

    Parameters
    ----------
    df_features : pandas.DataFrame
        Dataframe output of :func:`~.compute_features` or :func`~.compute_shape_features`.

    Returns
    -------
    df_features : pandas.DataFrame
        A dataframe without sample indices columns removed.
    df_samples : pandas.DataFrame
        A dataframe only containing sample indices columns.

    Examples
    --------
    Separate sample/signal indices into a separate dataframe:

    >>> from neurodsp.sim import sim_bursty_oscillation
    >>> from bycycle.features import compute_features
    >>> fs = 500
    >>> sig = sim_bursty_oscillation(10, fs, freq=10)
    >>> df_features = compute_features(sig, fs, f_range=(8, 12), center_extrema='peak')
    >>> df_features, df_samples = split_samples_df(df_features)
    """

    df_samples = pd.concat([df_features.pop(col) for col in df_features.columns.values \
        if "sample_" in col], axis=1)

    return df_features, df_samples
