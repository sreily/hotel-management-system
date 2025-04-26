from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, room_number, price):
        self.room_number = room_number
        self.price = price
        self.is_booked = False

    @abstractmethod
    def room_type(self):
        pass

    def book(self):
        self.is_booked = True

    def __str__(self):
        return f"{self.room_type()} Room {self.room_number} - ${self.price} - {'Booked' if self.is_booked else 'Available'}"

class SingleRoom(Room):
    def room_type(self):
        return "Single"

class DoubleRoom(Room):
    def room_type(self):
        return "Double"

class RoomFactory:
    @staticmethod
    def create_room(room_type, room_number, price):
        if room_type == "Single":
            return SingleRoom(room_number, price)
        elif room_type == "Double":
            return DoubleRoom(room_number, price)
        else:
            raise ValueError("Invalid room type")

class HotelManagementSystem:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(HotelManagementSystem, cls).__new__(cls)
            cls.__instance.rooms = []
            cls.__instance.load_rooms()
        return cls.__instance

    def load_rooms(self):
        try:
            with open('rooms.txt', 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    room_type, room_number, price, is_booked = data
                    room = RoomFactory.create_room(room_type, room_number, float(price))
                    room.is_booked = True if is_booked == 'True' else False
                    self.rooms.append(room)
        except FileNotFoundError:
            self.rooms = [
                RoomFactory.create_room("Single", "101", 100),
                RoomFactory.create_room("Double", "102", 150)
            ]

    def save_rooms(self):
        with open('rooms.txt', 'w') as file:
            for room in self.rooms:
                file.write(f"{room.room_type()},{room.room_number},{room.price},{room.is_booked}\n")

    def book_room(self, customer_name, room_type):
        for room in self.rooms:
            if not room.is_booked and room.room_type() == room_type:
                room.book()
                self.save_rooms()
                print(f"Room {room.room_number} booked successfully for {customer_name}.")
                return room
        print("No available rooms of this type.")
        return None

    def show_available_rooms(self):
        return [str(room) for room in self.rooms if not room.is_booked]
