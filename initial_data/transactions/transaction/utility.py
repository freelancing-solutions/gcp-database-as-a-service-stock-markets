import pandas as pd
df = pd.read_csv('transaction.csv', chunksize=10000)
[chunk.to_csv("transactions_{}.csv".format(count), index=None) for count, chunk in enumerate(df)]

