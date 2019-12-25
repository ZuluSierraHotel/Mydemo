from dataProcess import *
from modified_dbscan import *


def run(data, para_pool):
    para_pool = np.array(para_pool)
    cluster_result = []
    cluster_num = []
    radii = []
    if para_pool.ndim == 1:  # if the parameter dimension equals 1, the minPts parameter is default 2
        for idx, radius in enumerate(para_pool):
            clusterRes, clusterNum = m_dbscan(data, radius)
            radii.append(radius)
            cluster_result.append(clusterRes)
            cluster_num.append(clusterNum)
            print('epoch: ', idx + 1, '\t', 'cluster radius: ', radius, '\t', 'cluster number: ', clusterNum)
            print('cluster result: ', clusterRes)
            print('----------------------------')
    elif para_pool.ndim == 2:  # if the parameter dimension equals 2, the  parameters are custom
        for idx, radius in enumerate(para_pool):
            clusterRes, clusterNum = m_dbscan(data, *radius)
            radii.append(radius)
            cluster_result.append(clusterRes)
            cluster_num.append(clusterNum)
            print('epoch: ', idx + 1, '\t', 'cluster radius: ', radius, '\t', 'cluster number: ', clusterNum)
            print('cluster result: ', clusterRes)
            print('----------------------------')
    else:
        print('parameters error !')

    df_output = pd.DataFrame({'radii': radii, 'clusterRes': cluster_result, 'clusterNum': cluster_num})
    time_str = time.strftime("%Y%m%d-%H%M%S")
    df_output.to_csv('./data/result_{}.csv'.format(time_str))


if __name__ == '__main__':
    # data = pd.read_csv('data/processedDataframe.csv', index_col=0)
    data = pd.read_pickle('data/describeInfoN.pkl')
    para = range(30, 40, 10)
    run(data, para)
