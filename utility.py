"""Utility module for Kaggle ASHRAE competition.

Includes following functions:
    convert_bytes_size(size_bytes)
        Convert bytes to size string representation.
    optimize_columns_types(df[, verbose])
        Reduce size of numeric and string columns in Pandas DataFrame.
    plot_timeseries(datamart[, rows_df, plot_fcst, use_log_values])
        Plot meter readings vs time interactively.
    plot_derivatives(datamart, target_col, derivatives_cols)
        Plot derivatives interactively.

"""

import math
import pandas as pd
import cufflinks as cf
from ipywidgets import interact, widgets

def convert_bytes_size(size_bytes):
    """Convert bytes to size string representation."""
    if not size_bytes:
        return '0 B'
    size_names = ('B', 'KB', 'MB', 'GB', 'TB')
    i = min(int(math.floor(math.log(size_bytes, 1024))), len(size_names)-1)
    p = math.pow(1024, i)
    return f'{size_bytes/p:.1f} {size_names[i]}'

def optimize_columns_types(df, verbose=True):
    """Reduce size of numeric and string columns in Pandas DataFrame."""
    df_optimized = pd.DataFrame()
    for col in df.columns:
        col_type = df.dtypes[col].name
        if col_type.startswith('int'):
            df_optimized[col] = pd.to_numeric(df[col], downcast='integer')
        elif col_type.startswith('float'):
            df_optimized[col] = pd.to_numeric(df[col], downcast='float')
        elif (col_type == 'object' and
                len(df[col].unique()) / len(df[col]) < 0.5):
            df_optimized[col] = df[col].astype('category')
        else:
            df_optimized[col] = df[col]
    # Create dictionary of optimized columns types
    optimized_types = dict(zip(df_optimized.dtypes.index, [i.name for i in df_optimized.dtypes.values]))
    if verbose: 
        for col in df.columns:
            if df.dtypes[col].name != df_optimized.dtypes[col].name:
                print(f"Column {col} changed type from '{df.dtypes[col]}' to '{df_optimized.dtypes[col]}'")
    memory = df.memory_usage(deep=True).sum()   
    memory_optimized = df_optimized.memory_usage(deep=True).sum()
    coef = 100 * (memory - memory_optimized) / memory
    print(f'Memory usage decreased from {convert_bytes_size(memory)} to '
          f'{convert_bytes_size(memory_optimized)} ({coef:.0f}% reduction)')
    return df_optimized

def plot_timeseries(datamart, rows_df=None, plot_fcst=False, use_log_values=False):
    """Plot meter readings vs time interactively."""
    if use_log_values:
        fact_column = 'fact_log'
        leak_column = 'leak_log'
        target_column = 'target_log'
        fcst_column = 'fcst_log'
    else:
        fact_column = 'fact'
        leak_column = 'leak'
        target_column = 'target'
        fcst_column = 'fcst'
    if plot_fcst:
        cols = [target_column, fcst_column]
    else:
        cols = [leak_column, fact_column, target_column]
    df_to_plot = datamart.loc[:, ['meter', 'building_id', 'timestamp'] + cols]
    if rows_df is None:
        rows_df = datamart[['meter', 'building_id', 'site_id']].drop_duplicates()
    else:
        rows_df = rows_df.reset_index()[['meter', 'building_id', 'site_id']]
        df_to_plot = df_to_plot.merge(rows_df, on = ['meter', 'building_id'])
    df_to_plot.set_index('timestamp', inplace=True)
    meter_widget = widgets.RadioButtons(
        options=[('Electricity (0)', 0), ('Chilled water (1)', 1), 
                 ('Steam (2)', 2), ('Hot water (3)', 3)])
    building_id_widget = widgets.Select()
    
    def update_buildings_list(*args):
        building_id_widget.options = [
            (f"{row['building_id']}, site {row['site_id']}", row['building_id']) 
             for _, row in rows_df[rows_df.meter==meter_widget.value].iterrows()]
    meter_widget.observe(update_buildings_list, 'value')
    update_buildings_list()
    
    def plot_meter(meter, building_id):
        df_to_plot_selected = df_to_plot[(df_to_plot['meter'] == meter) & 
            (df_to_plot['building_id'] == building_id)][cols]
        if df_to_plot_selected[cols[0]].isna().all():
            df_to_plot_selected.loc['01.01.2016 00:00', cols[0]] = 0
        plot = df_to_plot_selected.iplot(
            asFigure=True, kind='scatter', 
            width=1, theme='ggplot',
            dimensions=(None, None), margin=(0, 0, 30, 30),  # l,r,b,t
        )
        plot['layout']['legend_orientation'] = 'h'
        display(plot)
        
    interact(plot_meter, meter=meter_widget, building_id=building_id_widget);

def plot_derivatives(datamart, target_col, derivatives_cols):
    """Plot derivatives interactively."""
    cols = [target_col] + derivatives_cols
    df_to_plot = datamart.loc[:, ['meter', 'site_id', 'building_id', 'timestamp'] + cols]
    df_to_plot.set_index('timestamp', inplace=True)
    rows_df = datamart[['meter', 'building_id', 'site_id']].drop_duplicates()
    meter_widget = widgets.RadioButtons(
        options=[('Electricity (0)', 0), ('Chilled water (1)', 1), 
                 ('Steam (2)', 2), ('Hot water (3)', 3)])
    building_id_widget = widgets.Select()
    
    def update_buildings_list(*args):
        building_id_widget.options = [
            (f"{row['building_id']}, site {row['site_id']}", row['building_id']) 
             for _, row in rows_df[rows_df.meter==meter_widget.value].iterrows()]
    meter_widget.observe(update_buildings_list, 'value')
    update_buildings_list()
    
    def plot_meter(meter, building_id):
        df_to_plot_selected = df_to_plot[(df_to_plot['meter'] == meter) & 
            (df_to_plot['building_id'] == building_id)][cols]
        if df_to_plot_selected[cols[0]].isna().all():
            df_to_plot_selected.loc['01.01.2016 00:00', cols[0]] = 0
        plot = df_to_plot_selected.iplot(
            asFigure=True, kind='scatter', 
            width=1, theme='ggplot',
            dimensions=(None, None), margin=(0, 0, 30, 30),  # l,r,b,t
        )
        plot['layout']['legend_orientation'] = 'h'
        display(plot)
    
    interact(plot_meter, meter=meter_widget, building_id=building_id_widget);