import pandas as pd
df = pd.read_csv('transaction.csv',chunksize=10000)
count = 1
for chunk in df:
    name = "transactions_{}.csv".format(count)
    chunk.to_csv(name, index=None)
    print(count)
    count += 1
