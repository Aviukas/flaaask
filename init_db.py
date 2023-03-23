
from app import app, db, User, Group
from models import User, Group

print("Creating app context...")
app_context = app.app_context()
app_context.push()

print("Creating database tables...")
db.create_all()

print("Adding sample data...")
group1 = Group(name="Group 1")
group2 = Group(name="Group 2")
db.session.add(group1)
db.session.add(group2)
user1 = User(username="user1_unique", password="password1")
user2 = User(username="user2_unique", password="password2")

db.session.add(user1)
db.session.add(user2)

user1.groups.append(group1)
user2.groups.append(group2)

db.session.commit()

print("Finished creating tables and sample data.")

app_context.pop()
