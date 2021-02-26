from datetime import date
from pony.orm import *
import os

db = Database()


class Event(db.Entity):
    id = PrimaryKey(str, auto=False)
    date = Required(date,default=date.today)
    organizer = Required('User')
    event_userss = Set('EventUsers')
    @property
    def n_infected(self):
        with db_session:
            n = select(i for i in db.EventUsers if i.infected).count()
            return n


class User(db.Entity):
    phone_number = PrimaryKey(str)
    is_organizer = Required(bool,default=False)
    events_organized = Set(Event)
    events = Set('EventUsers')

    
class EventUsers(db.Entity):
    event = Required(Event)
    user = Required(User)
    infected = Required(bool,default=False)
    PrimaryKey(event, user)


db.bind(provider='postgres', dsn=os.environ['DATABASE_URL'])
db.generate_mapping(create_tables=True)