import pandas as pd
import os

for files in os.listdir():
    if files.startswith('B_') and files.endswith('.csv'):
        df = pd.read_csv(files)
        if 'combined_df' not in locals():
            combined_df = df
        else:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
combined_df.to_csv('combined_B_instruments.csv', index=False)
for files in os.listdir():
    if files.startswith('N_') and files.endswith('.csv'):
        df = pd.read_csv(files)
        if 'combined_df' not in locals():
            combined_df = df
        else:
            combined_df = pd.concat([combined_df, df], ignore_index=True)
combined_df.to_csv('combined_N_instruments.csv', index=False)