# data_engine.py
import pandas as pd
import numpy as np
import datetime

def generate_billing_data(days, spike_val):
    """Generates mock billing data."""
    dates = pd.date_range(end=datetime.date.today(), periods=days)
    base_costs = np.random.randint(100, 120, size=days)
    df = pd.DataFrame({'date': dates, 'cost': base_costs})
    
    # Inject Spike on the last day
    df.iloc[-1, df.columns.get_loc('cost')] = spike_val
    return df

def detect_anomalies(df):
    """
    Calculates IQR and returns rows that are spikes.
    Returns: (spikes_dataframe, threshold_value)
    """
    Q1 = df['cost'].quantile(0.25)
    Q3 = df['cost'].quantile(0.75)
    IQR = Q3 - Q1
    threshold = Q3 + 1.5 * IQR
    
    spikes = df[df['cost'] > threshold]
    return spikes, threshold