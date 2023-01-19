from flask import Flask, render_template, request, redirect, url_for
import requests
from flask import session
import string

app = Flask(__name__)
app.secret_key = b'314159260'
rijec_dict = {}
slova_dict = {}
zivoti_dict = {}
tries_count_dict = {}  # broj pokusaja
win_count_dict = {}  # broj pobjeda
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


@app.route("/nova-igra", methods=['GET', 'POST'])
def nova_igra():
    username = session.get("username")
    if not username:
        return redirect(url_for('hello_world'))

    global slova_dict, rijec_dict, zivoti_dict, tries_count_dict
    d = None
    if request.method == "GET":
        slova_dict[username] = set(" ")
        rijec_dict[username] = get_word()
        zivoti_dict[username] = 10
        if odigrano := tries_count_dict.get(username):
            tries_count_dict[username] = odigrano + 1
        else:
            tries_count_dict[username] = 1

    if request.method == 'POST' and request.form['slovo']:
        d = request.form['slovo'].lower()
        slova_dict.get(username).add(d[0])
    n = ""

    rijec = rijec_dict.get(username)

    for a in rijec:
        if a.isspace() == True:
            n += "⨼ "
        elif a in slova_dict.get(username):
            n += f"{a} "
        else:
            n += "_ "

    if d != None and d not in rijec:
        zivoti_dict[username] = zivoti_dict.get(username) - 1

    x = ", ".join(slova_dict.get(username))
    pobjeda = "_" not in n

    if pobjeda == True:
        if pobjede := win_count_dict.get(username):
            win_count_dict[username] = pobjede + 1
        else:
            win_count_dict[username] = 1

    alphabet = list(string.ascii_uppercase)
    # print(tries_count_dict)
    context = {
        "rijec": rijec,
        "displej": n,
        "z": zivoti_dict.get(username),
        "x": x,
        "pobjeda": pobjeda,
        "tries_count_dict": tries_count_dict,
        "win_count_dict": win_count_dict,
        "alphabet": alphabet,
    }
    return render_template("nova_igra.html", context=context)


def get_word():
    api_url = 'https://random-word-api.herokuapp.com/word'
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print("nova rijec:", response.text)
        return response.text[2:-2]
    else:
        print("Error:", response.status_code, response.text)
        return "error"



