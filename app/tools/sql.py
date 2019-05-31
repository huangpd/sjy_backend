import pymysql


def execute_sql(sql_string):

    con = pymysql.connect(host='47.92.30.18', user='myuser', passwd='Shejiyuan201%1', db='town', port=3306) # 连接

    cur = con.cursor()

    result = cur.execute(sql_string)
    con.close()

    return result
