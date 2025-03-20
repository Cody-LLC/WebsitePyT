from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User
from . import db
from datetime import datetime

views = Blueprint('views', __name__)

def get_current_week_number():
    return datetime.now().isocalendar()[1]  # Get the current week number

@views.route('/', methods=['GET', 'POST'])
def home():
    # Check if user is an admin (from session)
    is_admin = session.get('is_admin', False)

    # Handle form submission for booking an appointment
    if request.method == 'POST':
        name = request.form.get('name')
        custom_time = request.form.get('custom_time')
        day = request.form.get('day')

        # Form validation
        if not name or len(name) <= 2:
            flash('Please input a valid name', category="error")
        elif custom_time and not custom_time.strip():
            flash('Please input a valid custom time', category="error")
        else:
            week_number = get_current_week_number()  # Get the current week number
            # Handle regular time or custom time
            if day in ['Friday', 'Saturday', 'Sunday']:
                time = 'custom'
            else:
                time = request.form.get('time')

            # Check if the timeslot is already booked
            existing_user = User.query.filter_by(day=day, time=time, week_number=week_number).first()
            if existing_user:
                flash(f"The {time} slot on {day} is already taken.", category="error")
            else:
                # If not booked, save the new appointment
                new_user = User(name=name, time=custom_time if custom_time else time, day=day, week_number=week_number)
                db.session.add(new_user)
                db.session.commit()
                flash("Appointment created successfully!", category="success")

                # Redirect back to the home page
                return redirect('/')

    # Handle appointment deletion for admins
    if is_admin and request.args.get('delete'):
        appointment_id = request.args.get('delete')
        appointment = User.query.get(appointment_id)
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            flash("Appointment deleted successfully!", category="success")
        else:
            flash("Appointment not found.", category="error")
        return redirect('/')

    # Fetch appointments for the current week
    week_number = get_current_week_number()
    users = User.query.filter_by(week_number=week_number).all()

    # Create a schedule dictionary with the booked users' names
    schedule = {
        "Monday": {"4:00PM": None, "5:00PM": None, "custom": None},
        "Tuesday": {"4:00PM": None, "5:00PM": None, "custom": None},
        "Wednesday": {"4:00PM": None, "5:00PM": None, "custom": None},
        "Thursday": {"4:00PM": None, "5:00PM": None, "custom": None},
        "Friday": {"4:00PM": None, "5:00PM": None, "custom": None},
        "Saturday": {"4:00PM": None, "5:00PM": None, "custom": None},
        "Sunday": {"4:00PM": None, "5:00PM": None, "custom": None},
    }

    # Populate the schedule dictionary with the names of users
    for user in users:
        if user.time == "4:00PM":
            schedule[user.day]["4:00PM"] = user
        elif user.time == "5:00PM":
            schedule[user.day]["5:00PM"] = user
        elif user.time == "custom":
            schedule[user.day]["custom"] = user

    return render_template("home.html", schedule=schedule, is_admin=is_admin)
