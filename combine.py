import pandas as pd
import os

for files in os.listdir():
    if files.endswith('.csv'):
        print(files)