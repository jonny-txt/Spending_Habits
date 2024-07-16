from flask import render_template, redirect, request, flash, session
from app import app
from app.models.user import User

@app.route('/login_register', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        action = request.form['action']
        if action == 'register':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            password_confirmation = request.form['password_confirmation']

            validation_errors = User.validate_user_data(first_name, last_name, email, password, password_confirmation)
            if validation_errors:
                for error in validation_errors:
                    flash(error, 'danger')
                return redirect('/login_register')

            hashed_password = User.hash_password(password)
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password_hash': hashed_password
            }
            User.save(data)
            flash('Registration successful! Please log in.', 'success')
            return redirect('/login_register')

        elif action == 'login':
            email = request.form['email']
            password = request.form['password']
            user = User.get_by_email(email)
            if user and User.check_password(password, user.password_hash):
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                return redirect('/home')
            flash('Invalid email or password', 'danger')
            return redirect('/login_register')

    return render_template('register_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login_register')
