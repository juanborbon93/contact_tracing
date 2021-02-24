
from .twilio import send_text, reply_to_text
from .db import db,select,db_session
from secrets import token_urlsafe
import os
from datetime import date,timedelta
import pytz

app_phone_number = os.environ.get("APP_PHONE_NUMBER")
def create_new_event(number):
    user = db.User.get(phone_number = number)
    if user and user.is_organizer:
        event_tokens = select(i.id for i in db.Event)
        unique_token = False
        while not unique_token:
            new_token = token_urlsafe(6)
            unique_token = new_token not in event_tokens
        with db_session:
            new_event = db.Event(id=new_token,organizer=user)
            db.commit()
            new_event_user = db.EventUsers(event=new_event,user=user)
            db.commit()
        response = reply_to_text(f"New event created. Attendees can register by texting {new_token} to {app_phone_number}")
    else:
        response = reply_to_text("You do not have event creation priviledges")
    return response

def register_attendee(number,token):
    with db_session:
        user = db.User.get(phone_number=number)
        if not user:
            user = db.User(phone_number=number)
        event = db.Event.get(id=token)
        new_event_user = db.EventUsers(event=event,user=user)
        db.commit()
    return reply_to_text(f"You have been registered for this event. If you contract COVID, text REPORT to {app_phone_number}")

def report_infection(number):
    today = datetime.now(tz=pytz.timezone('US/Central')).date()
    query_date = today-timedelta(days=14)
    user = db.User.get(phone_number=number)
    if user:
        exposed_attendances = select(i for i in db.EventUsers if i.user==user and i.event.date>query_date)
        for attendance in exposed_attendances:
            attendance.infected = True
            db.commit()
        exposed_events = [i.event for i in exposed_attendances]
        exposed_list = select(i for i in db.EventUsers if i.user!=user and i.event in exposed_events)
        for exposed in exposed_list:
            send_text(
                message=f"COVID exposure alert. {exposed.event.n_infected} infection(s) reported for {event.date} event",
                number= exposed.user.phone_number
            )
        n_exposed_events = len(exposed_events)
        if n_exposed_events == 0:
            response = reply_to_text(f"You did not attend any events in the last 14 days")
        else:
            response = reply_to_text(f"Alerted people who attended the {len(exposed_events)} that you attended in the last 14 days.")
    else:
        response = reply_to_text(f"You have not registered for any events")
    return response 


def handle_message(message,number):
    if message.lower() == "new":
        response = create_new_event(number)
    elif messe.lower() == "report":
        response = report_infection(number)
    else:
        event_codes = select(i.id for i in db.Event)
        if message in event_codes:
            response = register_attendee(number,message)
        else:
            response = reply_to_text(f'Invalid input: {message}')
    return response

        