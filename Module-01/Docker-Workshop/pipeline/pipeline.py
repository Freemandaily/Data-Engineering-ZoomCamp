import sys 
import pandas as pd

print('arguments:', sys.argv )

df =  pd.DataFrame({'day': [1, 2, 3], 'Num_passengers ': [10, 20, 30]})
month = sys.argv[1]
df['month'] = month

print(df.head())
df.to_parquet(f'output_{month}.parquet')

print(f'Processing data for month: {month}')