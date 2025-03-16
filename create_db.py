from website import create_app
from website.models import db

# Create the Flask app
app = create_app()

# Ensure you're in the app context before trying to create the tables
with app.app_context():
    db.create_all()  # This will create all tables in the database
    print("Database tables created successfully!")
