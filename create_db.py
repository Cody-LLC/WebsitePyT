from website import create_app
from website.models import db
app = create_app()
with app.app_context():
    db.create_all()  # This will create all tables in the database
    print("Database tables created successfully!")

    #from website import create_app
    #from website.models import db, Admin

   # app = create_app()

 #   with app.app_context():
  #      admin_user = Admin(email="admin@example.com", password="hashedpassword")
 #       db.session.add(admin_user)
  #      db.session.commit()
#
 #       print("Admin user created!")
