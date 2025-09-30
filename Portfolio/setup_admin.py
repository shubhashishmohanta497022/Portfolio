import getpass
from app import create_app, db
from models import User

def setup_admin():
    """
    Creates the first admin user for the application.
    This script should be run once during the initial setup.
    """
    app = create_app()
    with app.app_context():
        print("--- Create Admin User ---")
        
        # Check if an admin user already exists
        if User.query.first():
            print("An admin user already exists. Skipping.")
            return

        # Prompt for username and password
        username = input("Enter admin username: ")
        password = getpass.getpass("Enter admin password: ")
        confirm_password = getpass.getpass("Confirm admin password: ")

        # Validate password
        if password != confirm_password:
            print("Passwords do not match. Aborting.")
            return
            
        if not username or not password:
            print("Username and password cannot be empty. Aborting.")
            return

        # Create and save the new user
        admin_user = User(username=username)
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully!")
        print("You can now run the main application using 'python app.py'")

if __name__ == '__main__':
    setup_admin()
