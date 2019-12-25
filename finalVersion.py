import os
import pandas as pd


def makedir(path):
    """
    create a directory
    :param path: the path of directory
    :return: none
    """
    path = path.strip()  # remove the '' in head
    path = path.rstrip("\\")  # remove '/' in tail

    if not os.path.exists(path):  # if path doesn't exist, create the path
        os.makedirs(path)
        print(path + ' 创建成功')
    else:  # if path exists, print the message
        print(path + ' 目录已存在')


def demo(table_name):
    path = "D:/Documents/PycharmProjects/MyDissertation/output/" + table_name[9:]
    makedir(path)
    df = pd.DataFrame()
    df.to_csv(path + './hello.csv')


if __name__ == '__main__':
    starting_time = '2018-06-01 16:00:00'
    time_scheme = pd.date_range(starting_time, periods=3, freq='d')
    tableName_list = map(lambda time: time.strftime("AisRecord%Y%m%d"), time_scheme)
    for tn in tableName_list:
        demo(tn)
