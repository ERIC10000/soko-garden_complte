# Create an empty server
# Then run while debug is True:

from flask import *
import pymysql

def db_connection():
    return pymysql.connect(host='localhost', user='root', password='', database='soko_garden_db')

# start
app = Flask(__name__)
app.secret_key = "ghchghvvkgkjlkb.bbnn.n.n.n"

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/single')
def single():
    return render_template('single.html')

# Create a route:
# login
# register
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = db_connection()
        cursor = connection.cursor()

        sql = "select * from users where email = %s and password = %s"
        data = (email, password)
        cursor.execute(sql, data)

        # check ther user
        count = cursor.rowcount
        if count == 0:
            return render_template('login.html', message1 = 'Invalid Credentials')
        
        else:
            user = cursor.fetchone()
            session['key'] = user[1]
            return redirect('/')

    else:
        return render_template('login.html', message2 = 'Login Here' )


@app.route('/register', methods = ['POST', 'GET'])
def register():
    # step1: Check wether its POST or GET
    if request.method == 'POST':
        # step2: request data
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm = request.form['confirm']

        # Database Connection
        connection = db_connection()
        # cursor(): Give connection ability to run sql
        cursor = connection.cursor()
        sql = "insert into users (username, email, phone, password) values (%s, %s, %s, %s)"

        data = (username, email, phone, password)
        # Password Checks
        if password != confirm:
            return render_template('register.html', message = 'Password Dont March!')
        
        elif len(password) < 8:
            return render_template('register.html', message = 'Password Less than 8 characters!')
        
        else:
            cursor.execute(sql, data)
            connection.commit()
            return render_template('register.html', success = 'Register Successful')

    else:
        return render_template('register.html', message = 'Register Here')


app.run(debug=True)
# stop


