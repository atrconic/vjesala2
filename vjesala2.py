from flask import Flask, render_template, request, redirect, url_for
import requests
from flask import session

app = Flask(__name__)
app.secret_key = b'314159'
rijec_dict = {}
# r_d = {"a":"7", "g":"5"}
# x = r_d.get("a") --> "7"
# x = r_d.get("z") --> None
# x = r_d.get("7") --> None


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


@app.route("/nova-igra")
def nova_igra():
    global rijec_dict
    username = session.get("username")
    if not username:
        return redirect(url_for('hello_world'))
    if r := rijec_dict.get(username):
        return r
    else:
        rijec_dict[username] = get_word()
        return rijec_dict.get(username)


def get_word():
    api_url = 'https://random-word-api.herokuapp.com/word'
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print("nova rijec:", response.text)
        return response.text[2:-2]
    else:
        print("Error:", response.status_code, response.text)
        return "error"

