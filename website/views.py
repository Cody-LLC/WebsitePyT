from flask import Blueprint, render_template, request, flash, redirect, session
from .models import User
from .models import Availability
from . import db
from datetime import datetime

views = Blueprint('views', __name__) 

@views.route('/', methods=['GET', 'POST'])
def home():
    is_admin = session.get('is_admin', False)    # Check if user is an admin (from session)
    current_day = datetime.now().strftime('%A')  # This will give the current day of the week, e.g., 'Monday'
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
                # Remove extra spaces
                start_time = start_time.strip()
                end_time = end_time.strip()
                
                # Check if the availability entry already exists for this day
                availability = Availability.query.filter_by(day=day).first()

                if availability:
                    # If it exists, update the existing entry with the new times
                    availability.start_time = start_time
                    availability.end_time = end_time
                    db.session.commit()  # Save the changes
                    flash(f"Updated availability for {day}!", category="success")
                else:
                    # If it doesn't exist, create a new availability entry
                    new_availability = Availability(day=day, start_time=start_time, end_time=end_time)
                    db.session.add(new_availability)
                    db.session.commit()  # Save the new entry
                    flash(f"Set availability for {day}!", category="success")

            except ValueError:
                # Handle invalid time format (if the split fails)
                flash(f"Invalid time format for {day}. Please provide a time range like '11-5'.", category="error")
            
            return redirect('/')  # Redirect back to the home page after saving the time
    # Handle appointment deletion for admins
    if is_admin and request.args.get('delete'):
        item_id = request.args.get('delete')  # Get the item ID from the URL
        item_type = request.args.get('type')  # Get the type (either 'user' or 'availability')

        # Handle User deletion
        if item_type == 'user':
            user = User.query.get(item_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                flash("User deleted successfully!", category="success")
            else:
                flash("User not found.", category="error")

        # Handle Availability deletion
        elif item_type == 'availability':
            availability = Availability.query.get(item_id)
            if availability:
                db.session.delete(availability)
                db.session.commit()
                flash("Availability deleted successfully!", category="success")
            else:
                flash("Availability not found.", category="error")

        else:
            flash("Invalid delete type.", category="error")

        return redirect('/')  # Redirect to home or another page after deletion

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
    availability = {
        "Friday": [],
        "Saturday": [],
        "Sunday": []
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
    availability_slots = Availability.query.filter(Availability.day.in_(['Friday', 'Saturday', 'Sunday'])).all()
    for slot in availability_slots:
        day = slot.day
        start_time = slot.start_time  # Using start_time from the Availability model
        end_time = slot.end_time      # Using end_time from the Availability model
        if day in availability:
            availability[day].append({
                'start_time': start_time,  # The start time of the availability (e.g., '9:00AM')
                'end_time': end_time,      # The end time of the availability (e.g., '10:00AM')
                'id': slot.id              # Store the availability ID for deletion purposes (optional)
            })
    return render_template("home.html", schedule=schedule, availability=availability, is_admin=is_admin, current_day=current_day)
