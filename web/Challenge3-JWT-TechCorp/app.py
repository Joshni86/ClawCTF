"""
TechCorp Cloud Services - JWT Authorization Challenge
CTF Challenge: JWT Token Forgery & Role Escalation

This is an intentionally vulnerable web application for educational purposes.
DO NOT deploy this in a production environment.
"""

from flask import Flask, render_template, request, redirect, url_for, make_response
import jwt
import datetime
import os

app = Flask(__name__)

# VULNERABILITY: Weak JWT secret key
JWT_SECRET = "secret123"  # Intentionally weak secret
JWT_ALGORITHM = "HS256"

# Flag for the challenge
FLAG = "CLAWCTF{JWT_T0k3n_F0rg3ry}"

# In-memory user storage (for demo purposes)
users = {}

# Role hierarchy
ROLES = {
    'free': 0,
    'premium': 1,
    'business': 2,
    'enterprise': 3,
    'admin': 4
}


def create_jwt_token(username, role='free'):
    """
    Create a JWT token with user information.
    
    VULNERABILITY: Uses a weak secret key that can be brute-forced or guessed.
    """
    payload = {
        'username': username,
        'role': role,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    """
    Decode and verify JWT token.
    
    Returns the payload if valid, None if invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user():
    """Get current user from JWT token in cookies."""
    token = request.cookies.get('token')
    if not token:
        return None
    return decode_jwt_token(token)


@app.route('/')
def index():
    """Homepage - redirect to login or dashboard."""
    user = get_current_user()
    if user:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return render_template('signup.html', error='Username and password are required')
        
        if username in users:
            return render_template('signup.html', error='Username already exists')
        
        # Store user (in production, hash the password!)
        users[username] = password
        
        return redirect(url_for('login'))
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if username in users and users[username] == password:
            # Create JWT token with 'free' role
            token = create_jwt_token(username, role='free')
            
            response = make_response(redirect(url_for('dashboard')))
            response.set_cookie('token', token, httponly=True, max_age=86400)
            return response
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """User dashboard showing current role and available features."""
    user = get_current_user()
    
    if not user:
        return redirect(url_for('login'))
    
    role = user.get('role', 'free')
    username = user.get('username', 'User')
    
    # Role-specific features
    features = {
        'free': ['Basic Cloud Storage (5GB)', 'Email Support', 'Standard Security'],
        'premium': ['Enhanced Storage (50GB)', 'Priority Email Support', 'Advanced Security', 'API Access'],
        'business': ['Unlimited Storage', '24/7 Phone Support', 'Enterprise Security', 'Custom Integrations', 'Team Management'],
        'enterprise': ['Dedicated Infrastructure', 'Account Manager', 'SLA Guarantees', 'Advanced Analytics', 'White-label Options'],
        'admin': ['Full System Access', 'User Management', 'Security Vault', 'Audit Logs', 'System Configuration']
    }
    
    current_features = features.get(role, features['free'])
    role_level = ROLES.get(role, 0)
    
    return render_template('dashboard.html', 
                          username=username, 
                          role=role,
                          role_level=role_level,
                          features=current_features)


@app.route('/vault')
def vault():
    """Admin-only vault containing the flag."""
    user = get_current_user()
    
    if not user:
        return redirect(url_for('login'))
    
    role = user.get('role', 'free')
    username = user.get('username', 'User')
    
    # Check if user has admin role
    if role != 'admin':
        return render_template('forbidden.html', 
                              message=f'Access Denied! Your current role is "{role}". Admin role required to access the vault.',
                              current_role=role)
    
    # Admin access granted - show flag
    return render_template('vault.html', 
                          username=username, 
                          flag=FLAG)


@app.route('/logout')
def logout():
    """Clear session and redirect to login."""
    response = make_response(redirect(url_for('login')))
    response.set_cookie('token', '', expires=0)
    return response


@app.route('/robots.txt')
def robots():
    """
    Robots.txt with a hint about the JWT secret.
    
    This is an intentional hint for the CTF challenge.
    """
    return """User-agent: *
Disallow: /vault
Disallow: /admin

# Note to developers: Remember to change the JWT secret from 'secret123' before production!
# TODO: Use environment variable for JWT_SECRET
""", 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(host='0.0.0.0', port=port, debug=True)
