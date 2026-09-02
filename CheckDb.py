## TEST FIlE##
# Checking to see if the database is working properly

from db import get_connection, init_db, add_application, list_applications
from models import Application, Status
from datetime import date

conn = get_connection()
init_db(conn)

app = Application(
    company="My Application",
    role="Simple role",
    status=Status.APPLIED,
    date_applied=date.today(),
)

saved = add_application(conn, app)
print(f"Saved application: {saved} with ID: {saved.id}")

all_apps = list_applications(conn)
for a in all_apps:
    print(a)

conn.close