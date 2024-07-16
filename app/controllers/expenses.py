from flask import render_template, redirect, request, flash, session
from app import app
from app.models.expense import Expense
from app.config.mysqlconnection import connectToMySQL

def login_check():
    if 'user_id' not in session:
        flash('Please log in to view this page', 'info')
        return False
    return True

@app.route('/home')
def home():
    if not login_check():
        return redirect('/login_register')
    
    user_id = session['user_id']
    expenses = Expense.get_all(user_id)
    return render_template('home.html', expenses=expenses, first_name=session['first_name'])

@app.route('/expenses/new')
def new_expense():
    if not login_check():
        return redirect('/login_register')
    
    return render_template('new_expense.html', first_name=session['first_name'])

@app.route('/expenses/create', methods=['POST'])
def create_expense():
    if not login_check():
        return redirect('/login_register')

    data = {
        'name': request.form['name'],
        'cost': request.form['cost'],
        'date': request.form['date'],
        'user_id': session['user_id']
    }

    if not data['name'] or not data['cost'] or not data['date']:
        flash('All fields are required.', 'danger')
        return redirect('/expenses/new')

    try:
        data['cost'] = float(data['cost'])
        if data['cost'] <= 0:
            flash('Cost must be a positive number.', 'danger')
            return redirect('/expenses/new')
    except ValueError:
        flash('Cost must be a valid number.', 'danger')
        return redirect('/expenses/new')

    Expense.save(data)
    flash('Expense added successfully!', 'success')
    return redirect('/home')

@app.route('/expenses/<int:expense_id>')
def view_expense(expense_id):
    if not login_check():
        return redirect('/login_register')
    
    user_id = session['user_id']
    expense = Expense.get_by_id(expense_id, user_id)
    if not expense:
        flash('Expense not found', 'danger')
        return redirect('/home')

    return render_template('view_expense.html', expense=expense, first_name=session['first_name'])

@app.route('/expenses/edit/<int:expense_id>')
def edit_expense(expense_id):
    if not login_check():
        return redirect('/login_register')
    
    user_id = session['user_id']
    expense = Expense.get_by_id(expense_id, user_id)
    if not expense:
        flash('Expense not found', 'danger')
        return redirect('/home')

    return render_template('edit_expense.html', expense=expense, first_name=session['first_name'])

@app.route('/expenses/update/<int:expense_id>', methods=['POST'])
def update_expense(expense_id):
    if not login_check():
        return redirect('/login_register')
    
    user_id = session['user_id']
    expense = Expense.get_by_id(expense_id, user_id)
    if not expense:
        flash('Expense not found', 'danger')
        return redirect('/home')

    data = {
        'id': expense_id,
        'name': request.form['name'],
        'cost': request.form['cost'],
        'date': request.form['date'],
        'user_id': session['user_id']
    }

    if not data['name'] or not data['cost'] or not data['date']:
        flash('All fields are required.', 'danger')
        return redirect(f'/expenses/edit/{expense_id}')

    try:
        data['cost'] = float(data['cost'])
        if data['cost'] <= 0:
            flash('Cost must be a positive number.', 'danger')
            return redirect(f'/expenses/edit/{expense_id}')
    except ValueError:
        flash('Cost must be a valid number.', 'danger')
        return redirect(f'/expenses/edit/{expense_id}')

    Expense.update(data)
    flash('Expense updated successfully!', 'success')
    return redirect(f'/expenses/{expense_id}')

@app.route('/expenses/delete/<int:expense_id>')
def delete_expense(expense_id):
    if not login_check():
        return redirect('/login_register')
    
    user_id = session['user_id']
    expense = Expense.get_by_id(expense_id, user_id)
    if not expense:
        flash('Expense not found', 'danger')
        return redirect('/home')

    Expense.delete(expense_id, user_id)
    flash('Expense deleted successfully!', 'success')
    return redirect('/home')

@app.route('/expenses/date/<string:date>')
def expenses_by_date(date):
    if not login_check():
        return redirect('/login_register')
    
    user_id = session['user_id']
    query = """
        SELECT * FROM expenses 
        WHERE date = %(date)s AND user_id = %(user_id)s
    """
    expenses = connectToMySQL('spending').query_db(query, {'date': date, 'user_id': user_id})
    return render_template('expenses_by_date.html', expenses=expenses, date=date, first_name=session['first_name'])
