from flask import Flask, render_template, request, redirect, session
from hotel import HotelManagementSystem

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/hotel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = 'vgtucomputerengineeringekfu24/1'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_name = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    check_in = db.Column(db.String(20))
    check_out = db.Column(db.String(20))
    guests = db.Column(db.Integer)
    status = db.Column(db.String(20), default='confirmed')

    user = db.relationship('User', backref='reservations')

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

        user = User.query.filter_by(email=email, password=password).first()

        if user:
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
        elif User.query.filter_by(email=email).first():
            error = "Email already registered"
        else:
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
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

    user = User.query.filter_by(email=session['email']).first()

    new_reservation = Reservation(
        user_id=user.id,
        room_name=request.form['room_name'],
        full_name=request.form['full_name'],
        phone=request.form['phone'],
        check_in=request.form['check_in'],
        check_out=request.form['check_out'],
        guests=int(request.form['guests']),
    )

    db.session.add(new_reservation)
    db.session.commit()

    room_details = next(
        (details for key, details in room_info.items() if details['name'] == request.form['room_name']),
        None
    )

    return render_template('confirmation.html', room=room_details)


@app.route('/perform-cancel', methods=['POST'])
def perform_cancel():
    if 'email' not in session:
        return redirect('/login')

    user = User.query.filter_by(email=session['email']).first()
    check_in = request.form['cancel_check_in']
    check_out = request.form['cancel_check_out']

    reservation = Reservation.query.filter_by(
        user_id=user.id,
        check_in=check_in,
        check_out=check_out,
        status='confirmed'
    ).first()

    if reservation:
        reservation.status = 'cancelled'
        db.session.commit()

    return redirect('/my-reservations')


@app.route('/confirm-cancel', methods=['GET'])
def confirm_cancel():
    email = request.args.get('email')
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    return render_template('confirm_cancel.html', email=email, check_in=check_in, check_out=check_out)

@app.route('/my-reservations', methods=['GET', 'POST'])
def my_reservations():
    reservations = []
    email_searched = None

    if request.method == 'POST':
        email_searched = request.form['email']
        user = User.query.filter_by(email=email_searched).first()

        if user:
            reservations = Reservation.query.filter_by(user_id=user.id, status='confirmed').all()


    return render_template('my_reservations.html', reservations=reservations, email_searched=email_searched)



@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

