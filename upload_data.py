import mysql.connector as mysql
import pandas as pd
import numpy as np


def connect_to_mysql():
    db = mysql.connect(
        host="localhost",
        user="root",
        passwd="Mj887627",
        database="Slipher"
    )
    print(db)
    pointer = db.cursor()
    return pointer, db


def upload_data():
    data = pd.read_csv('/Users/marcinjedrzejewski/Desktop/Book1.csv')
    return data


if __name__ == '__main__':

    df = upload_data()
    cursor, database = connect_to_mysql()

    val = []

    for index, row in df.iterrows():
        series = (row['user_id'], row['date_actual'], row['subject'], row['time'])
        val.append(series)

    sql = "INSERT INTO activity_log (user_id, date_actual, subject, time) " \
          "VALUES(%s, STR_TO_DATE(%s, '%m/%d/%Y'), %s, %s)"

    cursor.executemany(sql, val)
    database.commit()


