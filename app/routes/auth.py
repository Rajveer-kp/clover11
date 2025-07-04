from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import db, User

auth = Blueprint('auth', __name__)

@auth.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            
            # Redirect based on user role
            if user.role == 'creator':
                return redirect(url_for('views.creator_dashboard'))
            elif user.role == 'editor':
                return redirect(url_for('views.editor_dashboard'))
            else:
                return redirect(url_for('auth.dashboard'))  # fallback
        else:
            flash("Invalid credentials")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        role = request.form.get('role')

        # Check if passwords match
        if password != confirm:
            flash("Passwords do not match!")
            return redirect(url_for('auth.register'))

        # Check if role is selected
        if not role or role not in ['creator', 'editor']:
            flash("Please select a valid account type!")
            return redirect(url_for('auth.register'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!")
            return redirect(url_for('auth.register'))

        # Create user instance and hash password
        new_user = User(name=name, email=email, role=role)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first.")
        return redirect(url_for('auth.login'))

    user = User.query.get(session['user_id'])
    
    # Redirect to role-specific dashboard
    if user.role == 'creator':
        return redirect(url_for('views.creator_dashboard'))
    elif user.role == 'editor':
        return redirect(url_for('views.editor_dashboard'))
    else:
        flash("Invalid user role.")
        return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('auth.login'))
