import numpy as np
from collections import Counter
from catchData import *


def enhanceData(sql_result):
    """
    group the result, and add new features: direction ,num of each vessel, the whole time spent in waterway
    :param sql_result: the decoded Ais data
    :return: a enhanced datafram, which is grouped and includes new features
    """
    keys_list = ['MMSI', 'ReceivedTime', 'SpeedOverGround', 'CourseOverGround', 'Longitude', 'Latitude']
    grouped = sql_result[keys_list].groupby(sql_result['MMSI'])  # group data by MMSI
    data = pd.DataFrame(grouped, columns=['MMSI', 'form'])  # change the group object into DataFrame

    # # this is a easier way to order/group the data, but i can't catch the key which i group by, so i dropped it.
    # another_df = rs[keys_list].sort_values(by=['MMSI', 'ReceivedTime'])

    data['direction'] = -1  # add feature
    data['num'] = -1  # add feature
    data['totalTime'] = -1  # add feature
    return data


def divideData(data, flag=200):
    """
    divide data by direction
    :param data: enhanced data
    :param flag: value of CourseOverGround
    :return: data in north and south
    """
    for index, value in data.iterrows():
        data.at[index, 'num'] = len(value['form'])
        data.at[index, 'totalTime'] = (
                value['form']['ReceivedTime'].max() - value['form']['ReceivedTime'].min()).total_seconds()
        if value['form']['CourseOverGround'].mean() > flag:  # divide the data by course
            # data.set_value(index, 'direction', 0)  # old method. the latest is below
            data.at[index, 'direction'] = 0
        else:
            # data.set_value(index, 'direction', 1)  # old method. the latest is below
            data.at[index, 'direction'] = 1

    data_N = data[data['direction'] == 0].reset_index(drop=True)
    data_S = data[data['direction'] == 1].reset_index(drop=True)
    # print(data_N, len(data_N), data_N['num'].describe())
    # print(velocity_mean_list)
    return data_N, data_S


def generateDescribeData(data):
    """
    generate some describe information of data, which is intended to split the outlier
    get some describe information of data
    :param data: the name of data
    :return: the list of mean velocity, mean course and the whole time spent in waterway
    """
    describe_info = {}
    velocity_mean_list = []
    velocity_std_list = []
    velocity_range_list = []
    course_mean_list = []
    course_std_list = []
    course_range_list = []
    total_time = []

    for index, value in data.iterrows():
        # vessl_velocity_list = value['form']['SpeedOverGround']
        # vessl_course_list = value['form']['CourseOverGround']
        # vessl_time_list = value['form']['ReceivedTime']

        velocity_mean_list.append(value['form']['SpeedOverGround'].mean())
        velocity_std_list.append(value['form']['SpeedOverGround'].std())
        velocity_range_list.append(value['form']['SpeedOverGround'].max() - value['form']['SpeedOverGround'].min())
        course_mean_list.append(value['form']['CourseOverGround'].mean())
        course_std_list.append(value['form']['CourseOverGround'].std())
        course_range_list.append(value['form']['CourseOverGround'].max() - value['form']['CourseOverGround'].min())
        total_time.append((value['form']['ReceivedTime'].max() - value['form']['ReceivedTime'].min()).total_seconds())

    describe_info["velocity_mean_list"] = velocity_mean_list
    describe_info["velocity_std_list"] = velocity_std_list
    describe_info["velocity_range_list"] = velocity_range_list
    describe_info["course_mean_list"] = course_mean_list
    describe_info["course_std_list"] = course_std_list
    describe_info["course_range_list"] = course_range_list
    describe_info["total_time"] = total_time

    return describe_info


def detect_outliers(df, n, features):
    outlier_indices = []

    # iterate over features(columns)
    for col in features:
        # 1st quartile (25%)
        Q1 = np.percentile(df[col], 25)
        # 3rd quartile (75%)
        Q3 = np.percentile(df[col], 75)
        # Interquartile range (IQR)
        IQR = Q3 - Q1

        # outlier step
        outlier_step = 1.5 * IQR

        # Determine a list of indices of outliers for feature col
        outlier_list_col = df[(df[col] < Q1 - outlier_step) | (df[col] > Q3 + outlier_step)].index

        # append the found outlier indices for col to the list of outlier indices
        outlier_indices.extend(outlier_list_col)

    # select observations containing more than 2 outliers
    outlier_indices = Counter(outlier_indices)
    multiple_outliers = list(k for k, v in outlier_indices.items() if v > n)

    return multiple_outliers


def prepareData(tableName):
    light_decoded_data = catchDataFromDB(tableName)
    # light_decoded_data.to_csv('data/decodedData.csv')
    enhanced_data = enhanceData(light_decoded_data)

    # # i have tried to save as csv, but the type of String hindered me
    # enhanced_data.to_csv('data/enhancedData.csv')
    #
    # # saving as pickle can keep all properties, it is more convenient.
    # enhanced_data.to_pickle('data/enhancedData.pkl')

    data_N, data_S = divideData(enhanced_data)
    return data_N, data_S


def dropOutliers(data, feature_list=None):
    if feature_list is None:
        feature_list = ['velocity_std_list', 'velocity_range_list', "total_time"]
    describe_info = generateDescribeData(data)
    info_df = pd.DataFrame(describe_info)
    # info_df.to_csv('data/describeInfoN.csv')
    outliers_to_drop = detect_outliers(info_df, 0, feature_list)
    processed_df = data.drop(outliers_to_drop, axis=0).reset_index(drop=True)
    return processed_df


if __name__ == '__main__':
    tableName = "AisRecord20180601"
    data_N, data_S = prepareData(tableName)
    processed_df_N = dropOutliers(data_N)
    processed_df_N.to_pickle('data/processedDF.pkl')
