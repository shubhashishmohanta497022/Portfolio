from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from extensions import db
from models import Project, Skill, Certification, Message, BlogPost, User
from slugify import slugify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length


# --- Form Classes ---

class LoginForm(FlaskForm):
    """Admin Login Form"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    github_link = StringField('GitHub Link')
    live_link = StringField('Live Link')
    image_url = StringField('Image URL')
    tags = StringField('Tags (comma-separated)')
    submit = SubmitField('Save Project')

class SkillForm(FlaskForm):
    name = StringField('Skill Name', validators=[DataRequired()])
    level = IntegerField('Proficiency Level (1-100)', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Save Skill')

class CertificationForm(FlaskForm):
    name = StringField('Certification Name', validators=[DataRequired()])
    issuer = StringField('Issuing Organization', validators=[DataRequired()])
    date_issued = DateField('Date Issued (YYYY-MM-DD)', validators=[DataRequired()], format='%Y-%m-%d')
    credential_link = StringField('Credential Link')
    submit = SubmitField('Save Certification')

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Save Post')


# --- Admin Blueprint ---
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# --- Main Admin Routes (Login, Logout, Dashboard) ---

@admin_bp.route('/')
def index():
    return redirect(url_for('admin.login'))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    # Redirect to the main portfolio homepage instead of the login page
    return redirect(url_for('portfolio.index'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    projects_count = Project.query.count()
    skills_count = Skill.query.count()
    certifications_count = Certification.query.count()
    messages_count = Message.query.filter_by(is_read=False).count()
    return render_template('admin/dashboard.html', 
                           projects_count=projects_count,
                           skills_count=skills_count,
                           certifications_count=certifications_count,
                           messages_count=messages_count)


# --- CRUD for Projects ---

@admin_bp.route('/projects')
@login_required
def list_projects():
    projects = Project.query.order_by(Project.date_created.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@admin_bp.route('/projects/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_bp.route('/projects/add', methods=['GET', 'POST'], defaults={'item_id': None})
@login_required
def edit_project(item_id):
    project = Project.query.get_or_404(item_id) if item_id else Project()
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        if not item_id:
            db.session.add(project)
        db.session.commit()
        flash('Project saved successfully!', 'success')
        return redirect(url_for('admin.list_projects'))
    return render_template('admin/edit_project.html', form=form, project=project)


# --- CRUD for Skills ---

@admin_bp.route('/skills')
@login_required
def list_skills():
    skills = Skill.query.order_by(Skill.name).all()
    return render_template('admin/skills.html', skills=skills)

@admin_bp.route('/skills/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_bp.route('/skills/add', methods=['GET', 'POST'], defaults={'item_id': None})
@login_required
def edit_skill(item_id):
    skill = Skill.query.get_or_404(item_id) if item_id else Skill()
    form = SkillForm(obj=skill)
    if form.validate_on_submit():
        form.populate_obj(skill)
        if not item_id:
            db.session.add(skill)
        db.session.commit()
        flash('Skill saved successfully!', 'success')
        return redirect(url_for('admin.list_skills'))
    return render_template('admin/edit_skill.html', form=form, skill=skill)


# --- CRUD for Certifications ---

@admin_bp.route('/certifications')
@login_required
def list_certifications():
    certifications = Certification.query.order_by(Certification.date_issued.desc()).all()
    return render_template('admin/certifications.html', certifications=certifications)

@admin_bp.route('/certifications/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_bp.route('/certifications/add', methods=['GET', 'POST'], defaults={'item_id': None})
@login_required
def edit_certification(item_id):
    certification = Certification.query.get_or_404(item_id) if item_id else Certification()
    form = CertificationForm(obj=certification)
    if form.validate_on_submit():
        form.populate_obj(certification)
        if not item_id:
            db.session.add(certification)
        db.session.commit()
        flash('Certification saved successfully!', 'success')
        return redirect(url_for('admin.list_certifications'))
    return render_template('admin/edit_certification.html', form=form, certification=certification)


# --- CRUD for Blog Posts ---

@admin_bp.route('/blog')
@login_required
def list_blog_posts():
    blog_posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('admin/blog_posts.html', blog_posts=blog_posts)

@admin_bp.route('/blog/edit/<int:item_id>', methods=['GET', 'POST'])
@admin_bp.route('/blog/add', methods=['GET', 'POST'], defaults={'item_id': None})
@login_required
def edit_blog_post(item_id):
    post = BlogPost.query.get_or_404(item_id) if item_id else BlogPost()
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        post.slug = slugify(post.title)
        if not item_id:
            db.session.add(post)
        db.session.commit()
        flash('Blog post saved successfully!', 'success')
        return redirect(url_for('admin.list_blog_posts'))
    return render_template('admin/edit_blog_post.html', form=form, post=post)


# --- Universal Delete Route ---

@admin_bp.route('/delete/<item_type>/<int:item_id>')
@login_required
def delete_item(item_type, item_id):
    item_map = {
        'project': (Project, 'admin.list_projects'),
        'skill': (Skill, 'admin.list_skills'),
        'certification': (Certification, 'admin.list_certifications'),
        'blogpost': (BlogPost, 'admin.list_blog_posts'),
        'message': (Message, 'admin.view_messages')
    }
    
    if item_type not in item_map:
        flash('Invalid item type.', 'danger')
        return redirect(url_for('admin.dashboard'))

    model, redirect_url = item_map[item_type]
    item = model.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash(f'{item_type.capitalize()} deleted successfully!', 'success')
    return redirect(url_for(redirect_url))


# --- Messages Route ---

@admin_bp.route('/messages')
@login_required
def view_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('admin/messages.html', messages=messages)
