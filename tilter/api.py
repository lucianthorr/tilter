from flask import Flask, g, render_template, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'pi'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'tiltdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
url_for('skeleton.css', static='css/skeleton.css')
mysql = MySQL()
mysql.init_app(app)

COLORS = ['red', 'green', 'black', 'purple', 'orange', 'blue', 'yellow', 'pink']

@app.route("/")
def index():
    tilts = get_tilts()
    print tilts
    return render_template('index.html', tilts=tilts)


def get_tilts():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT color FROM tilt")
    rv = cur.fetchall()
    tilts = [{"color": row[0]} for row in rv]
    conn.commit()
    conn.close()
    return tilts

def setup_table():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS tilt (color varchar(16), gravOffset float, tempOffset float)")
    cur.execute("CREATE TABLE IF NOT EXISTS stats (beer varchar(128), color varchar(16), unit varchar(16), gravity float, temp float)")
    conn.commit()
    conn.close()


if __name__ == '__main__':
    setup_table()
    app.run(debug=False, host='0.0.0.0', port= 5000, threaded=False)
