from flask import Flask, render_template, request, redirect
from hotel import HotelManagementSystem

app = Flask(__name__)
hotel = HotelManagementSystem()

@app.route('/')
def home():
    available_rooms = hotel.show_available_rooms()
    return render_template('index.html', rooms=available_rooms)

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    room_type = request.form['room_type']
    hotel.book_room(name, room_type)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
