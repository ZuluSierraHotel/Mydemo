import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

def addNoiseNumber(result_df):
    for index, value in result_df.iterrows():
        num = 0
        for mark in list(value['clusterRes']):
            if mark == '0':
                num += 1
        result_df.at[index, 'noiseNum'] = num
    return result_df


if __name__ == '__main__':
    result_df = pd.read_csv('./data/result_20191222-231721.csv', index_col=0)
    result_df = addNoiseNumber(result_df[:25])
    print(result_df)
    plt.figure()
    plt.plot(result_df['radii'], result_df['noiseNum'])
    plt.plot(result_df['radii'], result_df['clusterNum'])
    plt.show()


