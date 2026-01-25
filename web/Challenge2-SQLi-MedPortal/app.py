"""
Endurance Mission Control - Deep Space Research Terminal
CTF Challenge: SQL Injection Authentication Bypass

This is an intentionally vulnerable web application for educational purposes.
DO NOT deploy this in a production environment.

The system claims only authentication is possible.
But some channels carry more than their intended payload.
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
                             title='Endurance Mission Control - Authentication',
                             company_name=app.config['COMPANY_NAME'],
                             company_short=app.config['COMPANY_SHORT'])
    
    @app.route('/login', methods=['POST'])
    def login():
        """
        Handle authentication channel verification.
        
        This endpoint is vulnerable to SQL injection for educational purposes.
        The query assumes data flows in one direction only.
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
        """Display success page with recovered transmission."""
        if not session.get('authenticated'):
            return redirect(url_for('index'))
        
        return render_template('success.html', 
                             title='Signal Received - Endurance',
                             flag=app.config['FLAG_VALUE'],
                             username=session.get('username', 'Observer'))
    
    @app.route('/error')
    def error():
        """Display error page for failed authentication."""
        return render_template('error.html', 
                             title='No Signal Detected - Endurance')
    
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
