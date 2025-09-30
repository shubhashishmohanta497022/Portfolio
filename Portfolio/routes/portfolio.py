from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Project, Skill, Certification, Message, BlogPost, Visit
from app import db
import smtplib
from email.mime.text import MIMEText
from config import Config

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.before_request
def track_visit():
    """Simple middleware to track visits."""
    if request.endpoint and 'static' not in request.endpoint:
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        visit = Visit(ip_address=ip, user_agent=user_agent)
        db.session.add(visit)
        db.session.commit()

@portfolio_bp.route('/')
def index():
    """Renders the main portfolio page."""
    projects = Project.query.order_by(Project.date_created.desc()).all()
    
    # Group skills by category
    skills_query = Skill.query.all()
    skills = {}
    for skill in skills_query:
        if skill.category not in skills:
            skills[skill.category] = []
        skills[skill.category].append(skill)
        
    certifications = Certification.query.order_by(Certification.date_issued.desc()).all()
    blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(3).all()
    
    return render_template('index.html', 
                           projects=projects, 
                           skills=skills, 
                           certifications=certifications,
                           blog_posts=blog_posts)

@portfolio_bp.route('/contact', methods=['POST'])
def contact():
    """Handles the contact form submission."""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_body = request.form.get('message')

        if not name or not email or not message_body:
            flash('All fields are required.', 'danger')
            return redirect(url_for('portfolio.index') + '#contact')

        # Save message to database
        new_message = Message(name=name, email=email, message=message_body)
        db.session.add(new_message)
        db.session.commit()

        # Send email
        try:
            msg = MIMEText(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_body}")
            msg['Subject'] = f'New Portfolio Contact Message from {name}'
            msg['From'] = Config.MAIL_DEFAULT_SENDER
            msg['To'] = Config.MAIL_USERNAME

            with smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                server.starttls()
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
                server.send_message(msg)
            
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            print(f"Error sending email: {e}")
            flash('Your message was saved, but there was an error sending the email notification.', 'warning')

        return redirect(url_for('portfolio.index') + '#contact')
    return redirect(url_for('portfolio.index'))
