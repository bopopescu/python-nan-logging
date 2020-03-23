from flask import Flask
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')

def hello_world():
    cur = mysql.connection.cursor()
    cur.execute("select * from user_table");
    res = cur.fetchall()
    return res

if __name__ == '__main__':
     app.run(host='0.0.0.0')
