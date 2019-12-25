import numpy as np
import pandas as pd


def test1():
    global df
    df = pd.DataFrame(np.arange(12).reshape(3, 4), columns=['A', 'B', 'C', 'D'])
    print(df)
    df.drop([0, 1], inplace=True)
    print(df)


def test2():
    global df
    df = pd.DataFrame(np.arange(12).reshape(3, 4), columns=['A', 'B', 'C', 'D'])
    for index, value in df.iterrows():
        print(index)
        print(value['A'])



if __name__ == '__main__':

    # test1()
    # test2()
    a = list(range(10))
    print(a)
