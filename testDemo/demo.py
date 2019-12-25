import pandas as pd

df1 = pd.read_csv('../data/processedDataframe.csv', index_col=0)
df2 = pd.read_csv('../data/enhancedData.csv', index_col=0)
# print(df1)
# print(df2)

# time_max = df1.iloc[2, 1]['ReceivedTime']
time_max2 = df1.iloc[2, 1]
print(type(time_max2))

