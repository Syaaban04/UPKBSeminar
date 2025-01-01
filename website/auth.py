from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from . import db, mail
from . import models

auth = Blueprint('auth', __name__)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def create_new_password(token):
    user = models.User.query.filter_by(reset_token=token).first()
    if not user:
        flash('Invalid or expired token.', category='error')
        return redirect(url_for('auth.forgotpass'))

    if request.method == 'POST':
        new_password = request.form.get('pass')
        confirm_password = request.form.get('cpass')
        if new_password != confirm_password:
            flash('Passwords do not match.', category='error')
            return redirect(url_for('auth.create_new_password', token=token))

        user.password = new_password  # Hash the password in production
        user.reset_token = None  # Clear the token after reset
        db.session.commit()
        flash('Password updated successfully.', category='success')
        return redirect(url_for('auth.login'))

    return render_template('create_new_password.html', token=token)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    find_admin = models.User.query.filter_by(email='admin12@gmail.com').first()
    if not find_admin:
        new_admin = models.User(email='admin12@gmail.com', password='admin123')
        db.session.add(new_admin)       
        db.session.commit()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        session['email'] = email
        find_user = models.User.query.filter_by(email=email).filter_by(password=password).first()
        find_user2 = models.User.query.filter_by(email=email).first()

        if len(email) < 5:
            flash('Email must be greater than 4 characters', category="error")
        elif len(password) < 8:
            flash("Password must be greater than 8 characters", category="error")
        elif find_user:
            if find_user.email == 'admin12@gmail.com':
                return redirect(url_for('views.admin'))
            else:
                return redirect(url_for('views.home'))
        elif find_user2:
            flash(f'Wrong password', category='error')
        else:
            flash('The email entered does not exist', category='error')

    return render_template('login.html')

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        cpassword = request.form['cpass']

        find_user = models.User.query.filter_by(email=email).first()
        if find_user:
            flash("This email has already been taken", category='error')
            return render_template('signup.html')
        else:
            new_user = models.User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/forgotpass', methods=['GET', 'POST'])
def forgotpass():
    if request.method == 'POST':
        email = request.form.get('email')
        user = models.User.query.filter_by(email=email).first()
        if user:
            reset_token = models.generate_reset_token(user.email)
            user.reset_token = reset_token
            db.session.commit()

            reset_url = url_for('auth.create_new_password', token=reset_token, _external=True)

            msg = Message(
                subject="Password Reset Request",
                sender="nursyabanah174@gmail.com",
                recipients=[user.email],
                body=f"Click the link to reset your password: {reset_url}"
            )
            mail.send(msg)  # Use the mail object
            flash('Password reset link sent. Please check your email.', category='success')
        else:
            flash('Email does not exist.', category='error')
    return render_template('forgotpass.html')
