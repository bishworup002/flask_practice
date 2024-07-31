from app import create_app, db
from app.models import User, UserRole

app = create_app()

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Database initialized.")

@app.cli.command("create-admin")
def create_admin():
    admin = User(
        username="admin",
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        role=UserRole.ADMIN
    )
    admin.set_password("adminpassword")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created.")

if __name__ == '__main__':
    app.run(debug=True)