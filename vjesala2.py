from flask import Flask, render_template, request, redirect, url_for
from flask import session

app = Flask(__name__)
app.secret_key = b'314159'


@app.route("/")
def hello_world():
    username = session.get("username")
    return render_template('index2.html', username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('hello_world'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    if 'username' in session:
        session.pop('username', None)
    return redirect(url_for('hello_world'))

