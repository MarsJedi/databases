from flask import Flask, render_template, request
import os
import mysql.connector as mysql
from datetime import datetime
import dash_core_components
print(dash_core_components.__version__)


db = mysql.connect(
    host="localhost",
    user="root",
    passwd="Mj887627",
    database="Slipher"
)

cursor = db.cursor(prepared=True)
today = datetime.today().strftime('%m/%d/%Y')

app = Flask(__name__)


@app.route('/index', methods=['GET'])
def hello_world():

    t = (today,)
    query = """SELECT subject, SUM(time) AS total_time, (SUM(time)/10000)*100 FROM activity_log GROUP BY subject"""
    cursor.execute(query)
    data_all = cursor.fetchall()
    today_date = datetime.today().strftime('%m/%d/%Y')
    queryDaily = """SELECT subject, SUM(time) AS 'total time' FROM activity_log """ \
                 """WHERE date_actual = STR_TO_DATE(%s,'%m/%d/%Y') """ \
                 """GROUP BY subject"""
    cursor.execute(queryDaily, t)
    data_today = cursor.fetchall()

    return render_template("index.html", data_today=data_today, data_all=data_all)


@app.route('/record', methods=['POST', 'GET'])
def record():

    if request.method == 'GET':
        query = "SELECT subject FROM subjects"
        cursor.execute(query)
        subjects = cursor.fetchall()
        return render_template("record.html", subjects=subjects, today=today)

    elif request.method == "POST":
        date = request.form.get("date_field")
        subject = request.form.get("subject_field")
        time = request.form.get("time_field")

        print(date)
        print(subject)
        print(time)

        if date != "" and subject != "" and time != "":
            parameters = (date, subject, time)
            query = """INSERT INTO activity_log(user_id, date_actual, subject, time)""" \
                    """VALUES(1, STR_TO_DATE(%s, '%m/%d/%Y'), %s, %s)"""
            cursor.execute(query, parameters)
            db.commit()
            return render_template("success.html", date=date, subject=subject, time=time)
        else:
            missing_param = ""
            if date == "":
                missing_param = "date"
            elif subject == "":
                missing_param = "subject"
            elif time == "":
                missing_param = "time"

            return render_template("failed.html", missing_param=missing_param)


@app.route("/<subject_id>")
def subject(subject_id):

    param = (subject_id,)
    query = "SELECT date_actual, time FROM activity_log WHERE subject=%s"
    cursor.execute(query, param)
    data = cursor.fetchall()
    return render_template("subject.html", data=data, subject=subject_id)


if __name__ == '__main__':
    app.run()
