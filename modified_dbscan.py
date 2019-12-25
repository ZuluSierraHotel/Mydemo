import time
import queue
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
from dataProcess import *

NOISE = 0
UNASSIGNED = -1


def dtwdist(series1, series2):
    """
    calculate the distance of two series.
    :param series1: speed list of objection1
    :param series2: speed list of objection2
    :return: distance
    """
    # transform into array
    arr1 = np.array(series1)
    arr2 = np.array(series2)
    # regularization, minus the start value
    arr1 = arr1 - arr1[0]
    arr2 = arr2 - arr2[0]
    distance, path = fastdtw(arr1, arr2, dist=euclidean)
    return distance


def neighbor_points(data, pointId, radius):
    """
    得到邻域内所有样本点的Id
    :param data: 样本点
    :param pointId: 核心点
    :param radius: 半径
    :return: 邻域内所用样本Id
    """
    points = []
    time_max = data.iloc[pointId, 1]['ReceivedTime'].max()  # get the max of time
    time_min = data.iloc[pointId, 1]['ReceivedTime'].min()  # get the min of time
    center_speed_list = data.iloc[pointId, 1]['SpeedOverGround']  # get the speed list of core point
    for index, value in data.iterrows():
        if time_min < value['form']['ReceivedTime'].max() < time_max or time_min < value['form']['ReceivedTime'].min() < time_max:
            if dtwdist(value['form']['SpeedOverGround'], center_speed_list) < radius:
                points.append(index)
            else:
                pass
        else:
            continue
    return np.asarray(points)


def to_cluster(data, clusterRes, pointId, clusterId, radius, minPts):
    """
    判断一个点是否是核心点，若是则将它和它邻域内的所用未分配的样本点分配给一个新类
    若邻域内有其他核心点，重复上一个步骤，但只处理邻域内未分配的点，并且仍然是上一个步骤的类。
    :param data: 样本集合
    :param clusterRes: 聚类结果
    :param pointId:  样本Id
    :param clusterId: 类Id
    :param radius: 半径
    :param minPts: 最小局部密度
    :return:  返回是否能将点PointId分配给一个类
    """
    points = neighbor_points(data, pointId, radius)
    points = points.tolist()

    q = queue.Queue()

    if len(points) < minPts:
        clusterRes[pointId] = NOISE
        return False
    else:
        clusterRes[pointId] = clusterId
    for point in points:
        if clusterRes[point] == UNASSIGNED:
            q.put(point)
            clusterRes[point] = clusterId

    while not q.empty():
        neighborRes = neighbor_points(data, q.get(), radius)
        if len(neighborRes) >= minPts:  # 核心点
            for i in range(len(neighborRes)):
                resultPoint = neighborRes[i]
                if clusterRes[resultPoint] == UNASSIGNED:
                    q.put(resultPoint)
                    clusterRes[resultPoint] = clusterId
                elif clusterRes[clusterId] == NOISE:
                    clusterRes[resultPoint] = clusterId
    return True


def m_dbscan(data, radius, minPts=2):
    """
    扫描整个数据集，为每个数据集打上核心点，边界点和噪声点标签的同时为
    样本集聚类
    :param data: 样本集
    :param radius: 半径
    :param minPts:  最小局部密度
    :return: 返回聚类结果， 类id集合
    """
    clusterId = 1
    nPoints = len(data)
    clusterRes = [UNASSIGNED] * nPoints
    for pointId in range(nPoints):
        if clusterRes[pointId] == UNASSIGNED:
            if to_cluster(data, clusterRes, pointId, clusterId, radius, minPts):
                clusterId = clusterId + 1
    return np.asarray(clusterRes), clusterId


if __name__ == '__main__':
    # data = speedlist[:10]
    # print(len(speedlist))
    # with open('data/speedlist.csv','w') as f:
    #     f.write(str(data))
    # cluster = np.asarray(data[:, 2])
    # clusterRes, clusterNum = m_dbscan(data, 0.5, 3)
    # print(clusterRes, clusterNum)
    # path = 'data/data_grouped.pkl'
    path = 'data/propressed_data.pkl'
    data = pd.read_pickle(path)
    data_N, data_S = divideData(data)
    res = []
    num = []
    radiuses = []
    for radius in range(100, 150, 10):
        clusterRes, clusterNum = m_dbscan(data_N[:50], radius, 2)
        radiuses.append(radius)
        res.append(clusterRes)
        num.append(clusterNum)
        print(clusterRes, clusterNum)
        print('finish')

    # radiuses_s = pd.Series(range(10, 500, 10))
    # res_s = pd.Series(res)
    # num_s = pd.Series(num)
    # df_output = pd.DataFrame({'radius': radiuses_s, 'res': res_s, 'num': num_s})
    df_output = pd.DataFrame({'radius': radiuses, 'res': res, 'num': num})
    timestr = time.strftime("%Y%m%d-%H%M%S")
    df_output.to_csv('./data/result_{}.csv'.format(timestr))

