import pandas as pd
import numpy as np
import datetime

def generate_mock_billing_data(days=30):
    dates = pd.date_range(end=datetime.date.today(), periods=days)
    
    # Base cost: Normal steady usage ($100 - $120 per day)
    base_costs = np.random.randint(100, 120, size=days)
    
    # Create a DataFrame
    df = pd.DataFrame({'date': dates, 'cost': base_costs, 'service': 'EC2_Compute'})
    
    # Inject an anomaly (The Spike!)
    # On the last day, cost jumps to $500 because of a "memory leak"
    df.iloc[-1, df.columns.get_loc('cost')] = 500 
    
    return df

df = generate_mock_billing_data(20)
df.to_csv('cloud_bills.csv', index=False)
print("Mock data generated with a hidden spike!")