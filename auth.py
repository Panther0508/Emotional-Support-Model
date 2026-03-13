from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
        
    if request.method == 'POST':
        # If the request is JSON
        if request.is_json:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            user = User.query.filter_by(username=username).first()
            if user is None or not user.check_password(password):
                return jsonify({'success': False, 'message': 'Invalid username or password'})
                
            login_user(user, remember=True)
            return jsonify({
                'success': True, 
                'redirect': url_for('chat'),
                'username': user.username
            })
            
        # If it's a standard form submission
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=True)
        return redirect(url_for('chat'))
        
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
        
    if request.method == 'POST':
        # API request
        if request.is_json:
            data = request.get_json()
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Username and password are required'})
                
            if len(username) < 3 or len(username) > 30:
                return jsonify({'success': False, 'message': 'Username must be between 3 and 30 characters'})
                
            if User.query.filter_by(username=username).first():
                return jsonify({'success': False, 'message': 'Username already exists'})
                
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            
            login_user(user, remember=True)
            return jsonify({
                'success': True,
                'redirect': url_for('chat'),
                'message': 'Registration successful!'
            })
            
        # Form request
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
            
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user, remember=True)
        return redirect(url_for('chat'))
        
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
