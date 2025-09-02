from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    # Redirect to signin page if user is not authenticated
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    # If authenticated, redirect to dashboard
    return redirect(url_for('main.home'))

@bp.route('/landing')
def landing():
    """Public landing page for marketing/information purposes"""
    return render_template('index.html', title='Home')

@bp.route('/home')
@login_required
def home():
    return render_template('home.html', title='Dashboard', user=current_user)
