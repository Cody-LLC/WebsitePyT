from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Setup the database URI (using SQLite for this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable a warning
db = SQLAlchemy(app)

# Create the Appointment model (this defines the schema)
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # unique id for each appointment
    name = db.Column(db.String(100), nullable=False)  # name of the person
    date = db.Column(db.String(10), nullable=False)  # date of the appointment
    time = db.Column(db.String(5), nullable=False)  # time of the appointment

    def __repr__(self):
        return f'<Appointment {self.name} on {self.date} at {self.time}>'

# Initialize the database (this will create the appointments.db file and table)
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time = request.form['time']
        
        # Create a new Appointment object and add it to the database
        new_appointment = Appointment(name=name, date=date, time=time)
        db.session.add(new_appointment)  # Add to the session
        db.session.commit()  # Commit the session to save it to the database
        
        return redirect('/')
    
    return render_template('appointment.html')

@app.route('/appointments')
def show_appointments():
    # Query the database for all appointments
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()  # This ensures the table is created
