from flask import Blueprint, render_template, Flask, request, flash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    data = request.form
    print(data)
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        if type(time) != str:
            flash('Input a time i.e. 5:00 PM', category='error')
        elif type(name) == str:
            flash('Please input a valid name')
        else:
            flash("Appointment created")
    return render_template("home.html")