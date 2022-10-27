import pandas as pd

df = pd.read_csv('dataset.csv',',')

print(df['itemDescription'].to_string(index=False))
