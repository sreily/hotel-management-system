from flask import Flask, render_template, request, redirect, session
from hotel import HotelManagementSystem

app = Flask(__name__)
app.secret_key = 'vgtucomputerengineeringekfu24/1'

users = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect('/')
        else:
            return "Login failed! Wrong username or password."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        return redirect('/login')
    return render_template('register.html')

@app.route('/')
def home():
    if 'username' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    if 'username' not in session:
        return redirect('/login')
    return render_template('rooms.html')

@app.route('/rooms/<room_id>')
def room_details(room_id):
    ...

@app.route('/reservations')
def reservations():
    if 'username' not in session:
        return redirect('/login')
    return render_template('reservations.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
