Full-Stack Portfolio with Admin Panel
This is a complete, deployment-ready portfolio website built with Flask and Tailwind CSS. It features a dynamic public-facing portfolio and a secure admin panel for managing content.

Features
Public Portfolio:

Clean, responsive design with a light/dark mode theme switcher.

Dynamic sections for About Me, Skills, Projects, and Certifications, all managed from the admin panel.

Contact form that sends email notifications and stores messages in the database.

Admin Dashboard:

Secure login system.

Full CRUD (Create, Read, Update, Delete) functionality for Projects, Skills, Certifications, and Blog Posts.

View and manage contact form submissions.

Simple site analytics (visit counter).

Tech Stack:

Backend: Flask (Python)

Frontend: HTML, Tailwind CSS, JavaScript

Database: SQLAlchemy ORM with SQLite (easily switchable to PostgreSQL for production).

Authentication: Flask-Login

Migrations: Flask-Migrate

Project Structure
/
├── routes/
│   ├── admin.py        # Routes for the admin panel
│   └── portfolio.py    # Routes for the public site
├── static/             # (Optional) For custom CSS/JS/images
├── templates/
│   ├── admin/          # Admin panel templates
│   │   ├── *.html
│   └── *.html          # Public site templates
├── .env                # Environment variables (MUST create this)
├── .gitignore
├── app.py              # Main Flask app factory
├── config.py           # Configuration settings
├── models.py           # SQLAlchemy database models
├── requirements.txt    # Python dependencies
├── setup_admin.py      # Script to create the first admin user
└── README.md

Setup and Installation
1. Clone the repository:

git clone <your-repo-url>
cd <repo-name>

2. Create a virtual environment and activate it:

# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

3. Install the dependencies:

pip install -r requirements.txt

4. Create the .env file:

Create a file named .env in the root directory and add the following variables. This is crucial for configuration and security.

# Flask settings
SECRET_KEY='your_super_secret_key_here' # Generate a random string for this
FLASK_ENV='development' # Set to 'production' when deploying

# Database (for development, this is fine)
DEV_DATABASE_URL='sqlite:///portfolio_dev.db'

# Mail settings (for contact form) - Example for Gmail
MAIL_SERVER='smtp.gmail.com'
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME='your-email@gmail.com'
MAIL_PASSWORD='your-gmail-app-password' # Use an App Password for security

Note: For Gmail, you'll need to generate an "App Password". Go to your Google Account settings -> Security -> 2-Step Verification -> App passwords.

5. Initialize the database and create the admin user:

Run the setup_admin.py script and follow the prompts to create your administrator account. This only needs to be done once.

python setup_admin.py

6. Run the application:

python app.py

The application will be running at http://127.0.0.1:5000.

The public portfolio is at /.

The admin panel is at /admin.

Deployment
This application is ready for deployment on platforms like Railway, Render, or Heroku.

Set FLASK_ENV: Change the FLASK_ENV variable in your .env file (or your hosting provider's environment variables) to production.

Database URL: Set the DATABASE_URL environment variable to your production database URL (e.g., PostgreSQL). The config.py is already set up to use this.

Procfile: Create a Procfile in the root directory for your hosting provider:

web: gunicorn app:create_app()

Install Gunicorn: pip install gunicorn and add it to requirements.txt (pip freeze > requirements.txt).

Environment Variables: Ensure all variables from your .env file are set in your hosting provider's dashboard. Do not commit the .env file to version control.