import pandas as pd

df=pd.read_csv('transformed_data.csv', index_col=0)

df.to_csv('data_transofrmada.csv')

print(df.dtypes)
print(df.shape)