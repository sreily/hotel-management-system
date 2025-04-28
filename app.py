from flask import Flask, render_template, request, redirect, session
from hotel import HotelManagementSystem

app = Flask(__name__)
app.secret_key = 'vgtucomputerengineeringekfu24/1'

reservations_data = {}

users = {}

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

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/reservations', methods=['POST'])
def reservations():
    if 'username' not in session:
        return redirect('/login')
    
    username = session['username']

    reservation = {
        'room_name': request.form['room_name'],
        'full_name': request.form['full_name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'check_in': request.form['check_in'],
        'check_out': request.form['check_out'],
        'guests': request.form['guests'],
    }

    if username not in reservations_data:
        reservations_data[username] = []

    reservations_data[username].append(reservation)

    # Find correct room details based on room_name
    room_details = next(
        (details for key, details in room_info.items() if details['name'] == reservation['room_name']),
        None
    )

    return render_template('confirmation.html', room=room_details)


@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = None
    email_searched = None

    if request.method == 'POST':
        email = request.form['email']
        email_searched = email

        # Gather reservations matching the email
        reservations = []
        for user_reservations in reservations_data.values():
            for reservation in user_reservations:
                if reservation['email'] == email:
                    reservations.append(reservation)

    return render_template('my_reservations.html', reservations=reservations, email_searched=email_searched)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
