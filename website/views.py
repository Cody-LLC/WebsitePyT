from flask import Blueprint, render_template, Flask, request, flash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    data = request.form
    print(data)
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        if len(name) <= 2:
            print(f"Ran name {len(name)}")
            flash('Please input a valid name')
        elif time not in ["5:00PM", "7:00"]:
            flash('Only 5:00PM or 6:00PM is available', category='error')
            print(time)
        else:
            flash("Appointment created")
    return render_template("home.html")