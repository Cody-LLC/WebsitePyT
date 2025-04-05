from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User
from . import db
from datetime import datetime

views = Blueprint('views', __name__) 

@views.route('/', methods=['GET', 'POST'])
def home():
    # Check if user is an admin (from session)
    is_admin = session.get('is_admin', False)

    # Handle form submission for booking an appointment
    if request.method == 'POST':
        form_type = request.form.get('form-type')
        if form_type == "appointment":
            name = request.form.get('name')
            custom_time = request.form.get('custom_time')
            day = request.form.get('day')
            # Form validation
            if not is_admin and (not name or len(name) <= 2):  # Admin doesn't need to enter a name for custom times
                flash('Please input a valid name', category="error")
            elif custom_time and not custom_time.strip():
                flash('Please input a valid custom time', category="error")
            else:
                # Handle regular time or custom time
                if day in ['Friday', 'Saturday', 'Sunday']:
                    time = 'custom'
                else:
                    time = request.form.get('time')
                # Check if the timeslot is already booked
                existing_user = User.query.filter_by(day=day, time=time).first()
                if existing_user:
                    flash(f"The {time} slot on {day} is already taken.", category="error")
                else:
                    # If not booked, save the new appointment
                    new_user = User(name=name, time=custom_time if custom_time else time, day=day)
                    db.session.add(new_user)
                    db.session.commit()
                    users = User.query.all()
                    flash("Appointment created successfully!", category="success")
                    # Redirect back to the home page
                    return redirect('/')
        if form_type == "admin":
            day = request.form.get('day')  # Retrieve the value of the day from the hidden input
            custom_time = request.form.get('custom-time')  # Retrieve the value of the custom time input

            try:
                # Split the custom time into start and end times (assuming format is "11-5")
                start_time, end_time = custom_time.split('-')

                # Store start and end times in the session
                session[f'{day}_start_time'] = start_time.strip()  # Strip to remove any extra spaces
                session[f'{day}_end_time'] = end_time.strip()      # Strip to remove any extra spaces

                print(f"Day: {day}, Start Time: {start_time}, End Time: {end_time}")
                print(session)

            except ValueError:
                # Handle the case where the split operation fails (e.g., if there isn't a hyphen or only one number is provided)
                flash(f"Invalid time format for {day}. Please provide a time range like '11-5'.", category="error")
                # Optionally, you can store an error message in the session or set default times
            
            return redirect('/')  # Redirect back after saving the time
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
    users = User.query.all()

    # Create a schedule dictionary with the booked users' names
    schedule = {
        "Monday": {"4:00PM": None, "5:00PM": None, "custom": []},
        "Tuesday": {"4:00PM": None, "5:00PM": None, "custom": []},
        "Wednesday": {"4:00PM": None, "5:00PM": None, "custom": []},
        "Thursday": {"4:00PM": None, "5:00PM": None, "custom": []},
        "Friday": {"4:00PM": None, "5:00PM": None, "custom": []},
        "Saturday": {"4:00PM": None, "5:00PM": None, "custom": []},
        "Sunday": {"4:00PM": None, "5:00PM": None, "custom": []},
    }

    # Populate the schedule dictionary with the names of users
    for user in users:
        if user.time == "4:00PM":
            schedule[user.day]["4:00PM"] = user
        elif user.time == "5:00PM":
            schedule[user.day]["5:00PM"] = user
    custom_appointments = User.query.filter(User.day.in_(['Friday', 'Saturday', 'Sunday'])).all()
    for appointment in custom_appointments:
        day = appointment.day  # Get the day of the appointment (e.g., 'Friday')
        custom_time = appointment.time  # Get the custom time (e.g., '2:20')
        if day in schedule:
            schedule[day]['custom'].append({
                'name': appointment.name,  # Name of the user (e.g., 'Cody')
                'time': custom_time,      # The custom time (e.g., '2:20')
                'id': appointment.id  # Store the user's ID here for deletion purposes
            })

    return render_template("home.html", schedule=schedule, is_admin=is_admin)
