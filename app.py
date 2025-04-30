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
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email
            return redirect('/')
        else:
            error = "Incorrect Email Address or Password"
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if '@' not in email or '.' not in email:
            error = "Invalid Email Address"
        else:
            users[email] = password
            return redirect('/login')
    return render_template('register.html', error=error)

@app.route('/')
def home():
    if 'email' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    if 'email' not in session:
        return redirect('/login')
    return render_template('rooms.html')

@app.route('/rooms/<room_id>')
def room_details(room_id):
    if 'email' not in session:
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
    if 'email' not in session:
        return redirect('/login')
    
    email = session['email']

    reservation = {
        'room_name': request.form['room_name'],
        'full_name': request.form['full_name'],
        'email': request.form['email'],
        'phone': request.form['phone'],
        'check_in': request.form['check_in'],
        'check_out': request.form['check_out'],
        'guests': request.form['guests'],
    }

    if email not in reservations_data:
        reservations_data[email] = []

    reservations_data[email].append(reservation)

    room_details = next(
        (details for key, details in room_info.items() if details['name'] == reservation['room_name']),
        None
    )

    return render_template('confirmation.html', room=room_details)

@app.route('/cancel-reservation', methods=['POST'])
def cancel_reservation():
    if 'email' not in session:
        return redirect('/login')

    email = session['email']
    cancel_email = request.form['cancel_email']
    check_in = request.form['cancel_check_in']
    check_out = request.form['cancel_check_out']

    if email in reservations_data:
        reservations_data[email] = [
            r for r in reservations_data[email]
            if not (r['email'] == cancel_email and r['check_in'] == check_in and r['check_out'] == check_out)
        ]

    return redirect('/my-reservations')

@app.route('/confirm-cancel', methods=['GET'])
def confirm_cancel():
    email = request.args.get('email')
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    return render_template('confirm_cancel.html', email=email, check_in=check_in, check_out=check_out)

@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = None
    email_searched = None

    if request.method == 'POST':
        email = request.form['email']
        email_searched = email

        reservations = []
        for user_reservations in reservations_data.values():
            for reservation in user_reservations:
                if reservation['email'] == email:
                    reservations.append(reservation)

    return render_template('my_reservations.html', reservations=reservations, email_searched=email_searched)


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
