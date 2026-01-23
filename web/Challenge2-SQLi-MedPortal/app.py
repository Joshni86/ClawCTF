"""
Sacred Heart Medical - Electronic Health Records Portal
CTF Challenge: SQL Injection Authentication Bypass

This is an intentionally vulnerable web application for educational purposes.
DO NOT deploy this in a production environment.
"""

from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from config import config
import os


def create_app(config_name='default'):
    """Application factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize database
    with app.app_context():
        db.init_db()
    
    @app.route('/')
    def index():
        """Render the login page."""
        session.clear()
        return render_template('login.html', 
                             title='SHM Medical Portal - Secure Login',
                             company_name=app.config['COMPANY_NAME'],
                             company_short=app.config['COMPANY_SHORT'])
    
    @app.route('/login', methods=['POST'])
    def login():
        """
        Handle login authentication.
        
        This endpoint is vulnerable to SQL injection for educational purposes.
        """
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Attempt authentication (vulnerable to SQL injection)
        result = db.authenticate_user(username, password)
        
        if result:
            session['authenticated'] = True
            session['username'] = result[0]
            return redirect(url_for('success'))
        else:
            return redirect(url_for('error'))
    
    @app.route('/success')
    def success():
        """Display success page with flag."""
        if not session.get('authenticated'):
            return redirect(url_for('index'))
        
        return render_template('success.html', 
                             title='Access Granted - SHM Portal',
                             flag=app.config['FLAG_VALUE'],
                             username=session.get('username', 'User'))
    
    @app.route('/error')
    def error():
        """Display error page for failed login."""
        return render_template('error.html', 
                             title='Authentication Failed - SHM Portal')
    
    @app.route('/logout')
    def logout():
        """Clear session and redirect to login."""
        session.clear()
        return redirect(url_for('index'))
    
    return app


if __name__ == '__main__':
    # Get configuration from environment
    env = os.environ.get('FLASK_ENV', 'production')
    app = create_app(env)
    
    # Run the application
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
