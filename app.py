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
    if 'username' not in session:
        return redirect('/login')

    room_info = {
        'deluxe': {
            'name': 'Deluxe Ocean View',
            'price': 299,
            'size': '450 sq ft',
            'guests': 2,
            'bed_type': 'King Size Bed',
            'amenities': ['Free Wi-Fi', 'Ocean View', 'Flat-screen TV', 'Breakfast', 'Air Conditioning', 'Mini Bar'],
            'image': 'oceanview.jpg',
        },
        'standard': {
            'name': 'Standard Twin Room',
            'price': 199,
            'size': '350 sq ft',
            'guests': 2,
            'bed_type': 'Standard Bed',
            'amenities': ['Free Wi-Fi', 'Air Conditioning', 'Flat-screen TV', 'Coffee Maker'],
            'image': 'twinroom.jpg',
        },
        'suite': {
            'name': 'Premium King Suite',
            'price': 499,
            'size': '650 sq ft',
            'guests': 2,
            'bed_type': 'Luxury King Size Bed',
            'amenities': ['Free Wi-Fi', 'City View', 'Flat-screen TV', 'Breakfast', 'Air Conditioning', 'Mini Bar', 'Jacuzzi'],
            'image': 'kingsuite.jpg',
        }
    }

    room = room_info.get(room_id)
    if room:
        return render_template('room_details.html', room=room)
    else:
        return "Room not found", 404

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
