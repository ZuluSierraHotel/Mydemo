import pymssql
import pandas as pd

QUERY_ITEM = "ReceivedTime,MMSI,MessageType,Longitude,Latitude,SpeedOverGround,CourseOverGround"
CONDITION = "Longitude*0.1740+Latitude-59.0444<=0 AND \
             Longitude*0.1738+Latitude-58.9721>=0 AND \
             Longitude*0.5945+Latitude-109.7413>=0 AND \
             Longitude*(-4.8660)+Latitude+550.1418>=0"
def catchDataFromDB(tableName):
    """
    server    数据库服务器名称或IP
    user      用户名
    password  密码
    database  数据库名称
    :return:
    """
    database_para = {"server": '127.0.0.1:1433',
                     "user": 'sa',
                     "password": '0311',
                     "database": 'AisDB'
                     }
    # conn = pymssql.connect("127.0.0.1:1433", "sa", "0311", "AisDB")  # 连接数据库
    conn = pymssql.connect(**database_para)  # 连接数据库
    cursor = conn.cursor()  # 定义数据库游标
    sqlstr = sql_query(tableName)
    cursor.execute(sqlstr)  # execute the SQL command
    data = cursor.fetchall()  # get all data
    conn.close()  # close the connection
    sql_result = pd.DataFrame(data, columns=["ReceivedTime",
                                             "MMSI",
                                             "MessageType",
                                             "Longitude",
                                             "Latitude",
                                             "SpeedOverGround",
                                             "CourseOverGround"])  # put data into dataframe
    return sql_result


def sql_query(table_name, query_item=QUERY_ITEM, condition=CONDITION):  # 定义一个拼接SQL语句的函数
    """
    generate a SQL command.
    :param query_item: 要查询的目标字段
    :param table_name: 要查询的表名
    :param condition: 要查询的约束条件
    :return: 一条完整的SQL查询语句
    :return:
    """

    # sql_str = 'SELECT %s FROM %s WHERE %s ;' % (query_item, table_name, condition)
    sql_str = 'SELECT %s FROM %s WHERE %s ORDER BY ReceivedTime;' % (query_item, table_name, condition)
    return sql_str


if __name__ == '__main__':
    tableName = "AisRecord20180601"
    rs = catchDataFromDB(tableName)
    rs.to_csv('data/testdata.csv')
    print(rs)
