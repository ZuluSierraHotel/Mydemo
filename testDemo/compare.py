import pandas as pd

df1 = pd.read_pickle("../data/data_grouped.pkl")
df2 = pd.read_pickle("../data/propressed_data.pkl")

print(df1)
print(df2)