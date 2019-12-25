import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import timedelta, datetime
from pandas.plotting import register_matplotlib_converters
from mpl_toolkits.mplot3d import Axes3D

register_matplotlib_converters()

font = {'family': 'Times New Roman',  # the parameters of plot
        'weight': 'normal',
        'size': 20}


def plotDescribeData(describe_info):
    plt.subplot(221)
    plt.hist(describe_info['velocity_mean_list'], bins=20)
    plt.subplot(222)
    plt.hist(describe_info['course_mean_list'], bins=20)
    plt.subplot(223)
    plt.hist(describe_info['velocity_std_list'], bins=20)
    plt.subplot(224)
    plt.hist(describe_info['total_time'], bins=20)


def plotSpeedTimePicture(data):
    """
    plot the 'ReceivedTime'-'SpeedOverGround' picture of given data
    :param data:
    :return:
    """
    for index, value in data.iterrows():
        plt.plot(list(value['form']['ReceivedTime']), value['form']['SpeedOverGround'], lw=0.5)


def plotCourseTimePicture(data):
    """
    plot the 'ReceivedTime'-'CourseOverGround' picture of given data
    :param data: the processed data
    :return: none
    """
    for index, value in data.iterrows():
        plt.plot(list(value['form']['ReceivedTime']), value['form']['CourseOverGround'], lw=0.5)


def plotRes(data, clusterRes, clusterNum):
    """
    plot the result of clustering
    :param data: the processed data
    :param clusterRes: the list of cluster results
    :param clusterNum: the number of clusters
    :return: none
    """
    available_colors = ['black', 'blue', 'green', 'yellow', 'red', 'purple', 'orange', 'brown']
    for i in range(clusterNum):
        color = available_colors[i % len(available_colors)]
        for index, value in data.iterrows():
            if clusterRes[index] == i:
                plt.plot(list(value[1]['ReceivedTime']), value[1]['SpeedOverGround'], lw=0.5, color=color)


def trans2list(strings):
    """
    translate the string of '.csv' file into list
    :param strings: the string from '.csv'
    :return: the list of the values
    """
    ori_str = strings.replace(' ', ',')  # replace ' ' with ','
    ori_str = '{"transform":' + ori_str + '}'  # generate the format of json
    temp_json = json.loads(ori_str)
    new_list = temp_json.get('transform')
    # print(new_list, type(new_list))
    return new_list


def plotSpacePicture(data, clusterRes, clusterNum):
    ax = plt.axes(projection='3d')
    available_colors = ['black', 'blue', 'green', 'yellow', 'red', 'purple', 'orange', 'brown']
    for i in range(clusterNum):
        color = available_colors[i % len(available_colors)]
        for index, value in data.iterrows():
            if clusterRes[index] == i:
                lon = value['form']['Longitude']
                lat = value['form']['Latitude']
                time = value['form']['ReceivedTime']
                ax.plot(lon, lat, time, label='parametric curve', lw=0.5, color=color)
                # ax.legend()


def demo():
    result_df = pd.read_csv('data/result_20191222-231721.csv', index_col=0)
    data = pd.read_pickle('data/describeInfoN.pkl')
    for index, value in result_df.iterrows():
        # print(value, '\n', value['radius'])
        plt.figure(value['radii'])
        plotRes(data, trans2list(value['clusterRes']), value['clusterNum'])
        plt.xlabel('ReceivedTime')
        plt.ylabel('SpeedOverGround')
        plt.title('Result of clustering')
    plt.show()


if __name__ == '__main__':
    # demo()
    result_df = pd.read_csv('data/result_20191222-231721.csv', index_col=0)
    data = pd.read_pickle('data/processedDF.pkl')
    for index, value in result_df.iterrows():
        # print(value, '\n', value['radius'])
        plt.figure(value['radii'])
        plotSpacePicture(data, trans2list(value['clusterRes']), value['clusterNum'])
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Result of clustering')
    plt.show()


