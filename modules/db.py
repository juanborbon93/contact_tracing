from datetime import date
from pony.orm import *


db = Database()


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    date = Required(date)
    organizer = Required('User')
    event_userss = Set('EventUsers')


class User(db.Entity):
    phone_number = PrimaryKey(str, auto=True)
    events_organized = Set(Event)
    exposed = Required(bool,default=False)
    events = Set('EventUsers')


class EventUsers(db.Entity):
    event = Required(Event)
    user = Required(User)
    PrimaryKey(event, user)

db.generate_mapping()

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)