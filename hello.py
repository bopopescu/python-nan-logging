from flask import Flask, request, render_template
import mysql.connector as mariadb
import json
import datetime
app = Flask(__name__)

start_date = datetime.datetime.now() + datetime.timedelta(-30);



conn = mariadb.connect(
        user='root',
        password='root',
        database='test'
        )

cur = conn.cursor()

@app.route('/')

def hello_world():
    return render_template("index.html")

@app.route('/get404errors')


def get404():
    fname = request.args.get("fname")
    log_date = request.args.get("log_date")
    status = request.args.get("status")
    
    where = []
    params = {}
    

    if log_date != 'null':
        where.append("Date(log_date) = %(log_date)s")
        params['log_date'] = log_date

    if fname != 'null':
        where.append("filename = %(filename)s")
        params['filename'] = fname

    if status != 'null':
        where.append("apache_status = %(apache_status)s")
        params['apache_status'] = status
    
    sql = "SELECT * FROM apache_logs"
    
    if where:
        sql = '{} WHERE {}'.format(sql, ' AND '.join(where))
    
    cur.execute(sql,params)
    rows = cur.fetchall()   

    count = 0
    if fname != 'null':
       sql2 = "SELECT COUNT(*) FROM apache_logs WHERE filename=%s"
       val = (fname,)
       cur.execute(sql2, val)
 
       count = cur.fetchone()[0]
    print(count)


    """
    if log_date != 'null' and fname != 'null':
        sql = "select * from apache_logs where filename = %s and Date(log_date) = %s"
        val = (fname, log_date, )
    elif log_date == 'null' and fname != 'null':
        sql = "select * from apache_logs where filename = %s"
        val = (fname, )
    elif log_date != 'null' and fname == 'null':
        print(log_date)
        sql = "select * from apache_logs where Date(log_date) = %s"
        val = (log_date, )
    else:
        sql = "select * from apache_logs limit 10"
        val = ()
    cur.execute(sql, val)
    """
    json_data=[]
    for result in rows:
        json_data.append({'remote_host':result[1], 'apache_status':result[2], 'data_transfer':result[3], 'filename':result[4], 'log_date':str(result[5])})
        #json_data.append(dict(result))
    data = {}
    data['count'] = count
    data['data'] = json_data
    return json.dumps(data)
    #return json.dumps(json_data)

@app.route('/getComplete')
def getComplete():
    sql = "select CAST(log_date AS Date) as Date, count(*) as Total_Count, sum(case when apache_status=200 then 1 else 0 end) as Success, sum(case when apache_status=404 then 1 else 0 end) as failure from apache_logs group by Date"

    cur.execute(sql)
    rows = cur.fetchall()
    print(rows)
    
    json_data=[]
    for result in rows:
        json_data.append({'date':result[0].strftime('%m/%d/%Y'), 'total_count':result[1], 'success':str(result[2]),'failurer':str(result[3])})
        #json_data.append(dict(result))
        # data['count'] = count
        #data['data'] = json_data

    print(json_data)

    obj = {}
    obj['data'] = json_data
    return json.dumps(obj)
    #return json.dumps(json_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
