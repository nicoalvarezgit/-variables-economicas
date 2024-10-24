import pandas as pd


df=pd.read_csv('transformed_data_fed.csv', index_col=0)


df=df.dropna(axis=0,thresh=2)

print(df.shape)

print (df)