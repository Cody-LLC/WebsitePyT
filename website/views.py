from flask import Blueprint, render_template, request, flash, redirect
from .models import User
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

def get_current_week_number():
    return datetime.now().isocalendar()[1]    # This gives us the current week number of the year (1 to 52)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        day = request.form.get('day')
        # Form validation
        if len(name) <= 2:
            flash('Please input a valid name', category="error")
        elif time not in ["5:00PM", "7:00PM"]:
            flash('Only 5:00PM or 7:00PM is available', category='error')
        else:
            week_number = get_current_week_number()  # Get the current week number
            # Check if the timeslot is already booked
            existing_user = User.query.filter_by(day=day, time=time, week_number=week_number).first()
            if existing_user:
                flash(f"The {time} slot on {day} is already taken.", category="error")
            else:
                # If not booked, save the new appointment
                new_user = User(name=name, time=time, day=day, week_number=week_number)
                db.session.add(new_user)
                db.session.commit()
                flash("Appointment created successfully!", category="success")

                # Redirect back to the home page
                return redirect('/')

    # Fetch appointments for the current week
    week_number = get_current_week_number()
    users = User.query.filter_by(week_number=week_number).all()

    # Create a schedule dictionary with the booked users' names
    schedule = {
        "Monday": {"5:00PM": None, "7:00PM": None},
        "Tuesday": {"5:00PM": None, "7:00PM": None},
        "Wednesday": {"5:00PM": None, "7:00PM": None},
        "Thursday": {"5:00PM": None, "7:00PM": None},
        "Friday": {"5:00PM": None, "7:00PM": None},
        "Saturday": {"5:00PM": None, "7:00PM": None},
        "Sunday": {"5:00PM": None, "7:00PM": None},
    }

    # Populate the schedule dictionary with the names of users
    for user in users:
        if user.time == "5:00PM":
            schedule[user.day]["5:00PM"] = user.name
        elif user.time == "7:00PM":
            schedule[user.day]["7:00PM"] = user.name

    return render_template("home.html", schedule=schedule)
