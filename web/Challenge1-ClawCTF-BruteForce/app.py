from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = "flashsuperkeyforbruteforceattack"

@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>PaySecure - Merchant Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #f5f7fa;
            --card-bg: rgba(255,255,255,0.95);
            --border: #e6e9ef;
            --radius: 12px;
            --blue: #3758ff;
            --text-dark: #0f2347;
            --gray-400: #8f9bb3;
            --shadow: 0 30px 60px -10px rgba(15,35,71,0.15);
            font-family: 'Inter', system-ui,-apple-system,BlinkMacSystemFont,sans-serif;
        }
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            min-height: 100vh;
            background: #fff;
            color: #1f2d45;
        }
        .container {
            display: flex;
            min-height: 100vh;
        }
        .left {
            flex: 1.2;
            position: relative;
            background: url('https://6971c32f0fbe657fd5e60948.imgix.net/hero.jpg?auto=format&fit=crop&w=1400&q=80') center/cover no-repeat;
            display: flex;
            align-items: flex-end;
            padding: 40px 60px;
            color: white;
        }
        .left::after {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(15,35,71,0.4) 0%, rgba(15,35,71,0.65) 80%);
            mix-blend-mode: multiply;
        }
        .left-content {
            position: relative;
            max-width: 500px;
            z-index: 1;
        }
        .logo {
            position: absolute;
            top: 30px;
            left: 40px;
            z-index: 2;
            font-weight: 600;
            font-size: 20px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .logo img {
            height: 70px;
        }
        .headline {
            font-size: clamp(1.8rem, 1.9vw, 2.8rem);
            line-height: 1.1;
            font-weight: 600;
            margin: 0 0 12px;
        }
        .subline {
            font-size: 1.6rem;
            margin: 0;
            font-weight: 600;
            line-height: 1.1;
        }
        .highlight {
            color: #00c48f;
        }
        .features {
            margin-top: 30px;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 0.7rem;
        }
        .feature {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 500;
        }
        .feature svg {
            width: 16px;
            height: 16px;
            flex-shrink: 0;
        }
        .right {
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 60px 40px;
            background: url('https://6971c32f0fbe657fd5e60948.imgix.net/Card.jpg?auto=format&fit=crop&w=1000&q=80') center/cover no-repeat;
            overflow: hidden;
        }
        .right::after {
            content: '';
            position: absolute;
            inset: 0;
            background: rgba(245,247,250,0.5);
            backdrop-filter: blur(3px);
            pointer-events: none;
        }
        .card {
            background: var(--card-bg);
            border-radius: var(--radius);
            padding: 40px 40px 60px;
            width: 100%;
            max-width: 440px;
            position: relative;
            box-shadow: var(--shadow);
            z-index: 1;
        }
        .card .logo-small {
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg,#3758ff 0%, #2a46d0 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 16px;
        }
        .card .logo-small svg {
            width: 24px;
            height: 24px;
            fill: white;
        }
        .welcome {
            font-size: 12px;
            color: var(--gray-400);
            margin: 0 0 4px;
        }
        .welcome b {
            font-weight: 600;
            color: var(--text-dark);
        }
        .title {
            font-size: 2rem;
            font-weight: 700;
            margin: 0 0 30px;
            line-height: 1.1;
            color: var(--text-dark);
        }
        .input-wrapper {
            margin-bottom: 20px;
        }
        .input-wrapper input {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #d9e2ec;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            background: #f9fbfd;
            color: #2a3a57;
            transition: border-color .2s, box-shadow .2s;
        }
        .input-wrapper input:focus {
            border-color: #a3b1d1;
            box-shadow: 0 0 0 3px rgba(55,88,255,0.15);
        }
        .btn {
            width: 100%;
            padding: 14px 16px;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            background: var(--blue);
            color: white;
            letter-spacing: .5px;
            transition: filter .2s;
        }
        .btn:hover {
            filter: brightness(1.05);
        }
        .footer {
            margin-top: 40px;
            font-size: 12px;
            color: #8f9bb3;
            text-align: center;
            line-height: 1.4;
            padding-bottom: 4px;
        }
        .footer a {
            color: #3758ff;
            text-decoration: none;
            font-weight: 600;
        }
        @media (max-width: 1100px) {
            .left {
                display: none;
            }
            .container {
                flex-direction: column;
            }
            .right {
                padding: 60px 20px;
                background: #f5f7fa;
            }
            .right::after {
                background: rgba(255,255,255,1);
            }
            .card {
                margin: 0 auto;
                width: 100%;
                max-width: 480px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left" aria-hidden="true">
            <div class="logo">
                <span style="font-size: 2rem;">💳 PaySecure</span>
            </div>
            <div class="left-content">
                <h1 class="headline">Join <span class="highlight">8 Million</span> Businesses that Trust</h1>
                <h1 class="subline">PaySecure to Power their Payments</h1>
                <div class="features">
                    <div class="feature">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M6.003 11.803L2.2 8l1.4-1.4L6 9.003l6.4-6.4L14 4.6z"/></svg>
                        <div>100+ Payment Methods</div>
                    </div>
                    <div class="feature">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M6.003 11.803L2.2 8l1.4-1.4L6 9.003l6.4-6.4L14 4.6z"/></svg>
                        <div>Easy Integration</div>
                    </div>
                    <div class="feature">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M6.003 11.803L2.2 8l1.4-1.4L6 9.003l6.4-6.4L14 4.6z"/></svg>
                        <div>Powerful Dashboard</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="right">
            <div class="card" aria-label="signup card">
                <div style="display:flex; align-items:center; gap:12px;">
                    <div class="logo-small" aria-hidden="true">
                        <svg viewBox="0 0 24 24" aria-label="icon">
                            <path d="M12 2L3 21h18L12 2z"/>
                        </svg>
                    </div>
                    <div>
                        <div class="welcome">Welcome to <b>PaySecure Merchant Portal</b></div>
                    </div>
                </div>
                <h2 class="title">Merchant Dashboard Login</h2>
                <form action="/login" method="post">
                    <div class="input-wrapper">
                        <input type="text" name="username" placeholder="Username" required>
                    </div>
                    <div class="input-wrapper">
                        <input type="password" name="password" placeholder="Password" required>
                    </div>
                    <div class="input-wrapper">
                        <button class="btn" type="submit">Continue</button>
                    </div>
                </form>
                <div class="footer">
                    By continuing you agree to our <a href="#">privacy policy</a> and <a href="#">terms of use</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    if username == "admin" and password == "password":
        session["logged_in"] = True
        session["balance"] = 0.00
        session["vault_unlocked"] = False
        return redirect("/dashboard")
    else:
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Failed - PaySecure</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f5f7fa;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .error-box {
            background: white;
            border-radius: 8px;
            padding: 32px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            text-align: center;
        }
        .icon {
            width: 48px;
            height: 48px;
            background: #fee;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
            color: #dc2626;
            font-size: 24px;
        }
        h1 {
            font-size: 20px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 8px;
        }
        p {
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 24px;
            line-height: 1.5;
        }
        a {
            display: inline-block;
            background: #3758ff;
            color: white;
            padding: 10px 20px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            font-size: 14px;
            transition: background 0.2s;
        }
        a:hover {
            background: #2a46d0;
        }
    </style>
</head>
<body>
    <div class="error-box">
        <div class="icon">×</div>
        <h1>Authentication Failed</h1>
        <p>The username or password you entered is incorrect. Please try again.</p>
        <a href="/">Return to Login</a>
    </div>
</body>
</html>
"""

@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    
    balance = session.get("balance", 0.00)
    vault_unlocked = session.get("vault_unlocked", False)
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - PaySecure</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0a url('https://6971c32f0fbe657fd5e60948.imgix.net/splash') center/cover fixed no-repeat;
            color: #1a1a1a;
            position: relative;
        }}
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.6);
            z-index: 0;
        }}
        body > * {{
            position: relative;
            z-index: 1;
        }}
        .header {{
            background: white;
            border-bottom: 1px solid #e5e7eb;
            padding: 0 24px;
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .header-left {{
            display: flex;
            align-items: center;
            gap: 32px;
        }}
        .logo {{
            font-weight: 600;
            font-size: 18px;
            color: #1a1a1a;
        }}
        .nav {{
            display: flex;
            gap: 24px;
        }}
        .nav a {{
            color: #6b7280;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .nav a.active {{
            color: #1a1a1a;
        }}
        .user-menu {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .user-btn {{
            background: #f3f4f6;
            border: none;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            color: #374151;
            font-weight: 500;
        }}
        .logout {{
            color: #6b7280;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 32px 24px;
        }}
        .page-title {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #111827;
        }}
        .page-subtitle {{
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 32px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin-bottom: 24px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 24px;
        }}
        .card-label {{
            font-size: 13px;
            color: #6b7280;
            font-weight: 500;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .card-value {{
            font-size: 32px;
            font-weight: 700;
            color: #111827;
        }}
        .card-value.green {{
            color: #059669;
        }}
        .card-meta {{
            font-size: 13px;
            color: #9ca3af;
            margin-top: 4px;
        }}
        .vault-card {{
            grid-column: 1 / -1;
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            position: relative;
            overflow: hidden;
        }}
        .vault-card::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        }}
        .vault-content {{
            position: relative;
            z-index: 1;
        }}
        .vault-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}
        .vault-title {{
            font-size: 20px;
            font-weight: 600;
        }}
        .vault-badge {{
            background: rgba(251, 191, 36, 0.2);
            color: #fbbf24;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .vault-desc {{
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .price-row {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 20px;
        }}
        .price {{
            font-size: 36px;
            font-weight: 700;
        }}
        .btn {{
            background: #fbbf24;
            color: #1a1a1a;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: background 0.2s;
        }}
        .btn:hover {{
            background: #f59e0b;
        }}
        .flag-box {{
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 6px;
            padding: 16px;
            margin-top: 20px;
        }}
        .flag-box h4 {{
            color: #10b981;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .flag-box code {{
            display: block;
            background: rgba(0,0,0,0.2);
            padding: 12px;
            border-radius: 4px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            color: #a7f3d0;
            word-break: break-all;
        }}
        .info-box {{
            background: #eff6ff;
            border: 1px solid #dbeafe;
            border-radius: 8px;
            padding: 16px;
            font-size: 13px;
            color: #1e40af;
            line-height: 1.6;
        }}
        @media (max-width: 768px) {{
            .nav {{ display: none; }}
            .grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="header-left">
            <div class="logo">💳 PaySecure</div>
            <nav class="nav">
                <a href="/dashboard" class="active">Dashboard</a>
                <a href="#">Transactions</a>
                <a href="#">Settings</a>
            </nav>
        </div>
        <div class="user-menu">
            <button class="user-btn">admin</button>
            <a href="/logout" class="logout">Logout</a>
        </div>
    </header>
    
    <div class="container">
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Overview of your merchant account</p>
        
        <div class="grid">
            <div class="card">
                <div class="card-label">Account Balance</div>
                <div class="card-value green">${balance:.2f}</div>
                <div class="card-meta">Available funds</div>
            </div>
            
            <div class="card">
                <div class="card-label">Account Type</div>
                <div class="card-value" style="font-size: 24px;">Free</div>
                <div class="card-meta">Standard merchant account</div>
            </div>
            
            <div class="card vault-card">
                <div class="vault-content">
                    <div class="vault-header">
                        <div class="vault-title">Premium Vault Access</div>
                        <div class="vault-badge">
                            {"🔓 Unlocked" if vault_unlocked else "🔒 Locked"}
                        </div>
                    </div>
                    <p class="vault-desc">
                        Unlock access to premium API keys, advanced analytics, and confidential merchant data.
                    </p>
                    <div class="price-row">
                        <span class="price">$99.00</span>
                        {"" if vault_unlocked else '<a href="/payment" class="btn">Unlock Now</a>'}
                    </div>
                    
                    {"<div class='flag-box'><h4>✓ Vault Unlocked Successfully</h4><code>CLAWCTF{Pr1c3_M4nipul4ti0n_Mast3r}</code></div>" if vault_unlocked else ""}
                </div>
            </div>
        </div>
        
        <div class="info-box">
            💡 Premium features require sufficient account balance to unlock. Add funds to your wallet to access exclusive merchant tools.
        </div>
    </div>
</body>
</html>
"""

@app.route("/payment")
def payment():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    
    if session.get("vault_unlocked"):
        return redirect("/dashboard")
    
    balance = session.get("balance", 0.00)
    
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment - PaySecure</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0a0a0a url('https://6971c32f0fbe657fd5e60948.imgix.net/xcard') center/cover fixed no-repeat;
            color: #1a1a1a;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            position: relative;
        }}
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.4);
            z-index: 0;
        }}
        body > * {{
            position: relative;
            z-index: 1;
        }}
        .payment-container {{
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 32px;
            width: 100%;
            max-width: 480px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .header-icon {{
            width: 48px;
            height: 48px;
            background: #f3f4f6;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px;
            font-size: 24px;
        }}
        .header h1 {{
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 4px;
            color: #111827;
        }}
        .header p {{
            color: #6b7280;
            font-size: 14px;
        }}
        .summary {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
        }}
        .summary-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            font-size: 14px;
        }}
        .summary-row:last-child {{
            margin-bottom: 0;
            padding-top: 12px;
            border-top: 1px solid #e5e7eb;
            font-weight: 600;
        }}
        .summary-label {{
            color: #6b7280;
        }}
        .summary-value {{
            color: #111827;
            font-weight: 500;
        }}
        .summary-value.balance {{
            color: #059669;
        }}
        .summary-value.required {{
            color: #dc2626;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        .form-group label {{
            display: block;
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            margin-bottom: 6px;
        }}
        .form-group input {{
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            font-family: inherit;
            color: #1a1a1a;
            transition: border-color 0.2s;
        }}
        .form-group input:focus {{
            outline: none;
            border-color: #3758ff;
            box-shadow: 0 0 0 3px rgba(55, 88, 255, 0.1);
        }}
        .btn {{
            width: 100%;
            padding: 12px;
            background: #3758ff;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn:hover {{
            background: #2a46d0;
        }}
        .security-note {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #9ca3af;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}
        .back-link {{
            display: block;
            text-align: center;
            margin-top: 16px;
            color: #6b7280;
            text-decoration: none;
            font-size: 14px;
        }}
        .back-link:hover {{
            color: #3758ff;
        }}
    </style>
</head>
<body>
    <div class="payment-container">
        <div class="header">
            <div class="header-icon">🔒</div>
            <h1>Unlock Premium Vault</h1>
            <p>Complete payment to access exclusive features</p>
        </div>
        
        <div class="summary">
            <div class="summary-row">
                <span class="summary-label">Item</span>
                <span class="summary-value">Premium Vault Access</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Your Balance</span>
                <span class="summary-value balance">${balance:.2f}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Total</span>
                <span class="summary-value required">$99.00</span>
            </div>
        </div>
        
        <form action="/process-payment" method="POST" onsubmit="return validatePayment()">
            <div class="form-group">
                <label for="card">Card Number</label>
                <input type="text" id="card" name="card" placeholder="4242 4242 4242 4242" value="4242424242424242">
            </div>
            
            <div class="form-group">
                <label for="amount">Payment Amount ($)</label>
                <input type="number" id="amount" name="amount" value="99" min="99" step="0.01" required>
            </div>
            
            <input type="hidden" name="product_price" value="99.00">
            
            <button type="submit" class="btn" id="payBtn">Pay $99.00</button>
        </form>
        
        <p class="security-note">
            <span>🔒</span>
            <span>Secured by 256-bit SSL encryption</span>
        </p>
        <a href="/dashboard" class="back-link">← Back to Dashboard</a>
    </div>
    
    <script>
        function validatePayment() {{
            const amount = parseFloat(document.getElementById('amount').value);
            const requiredAmount = 99.00;
            
            if (amount < requiredAmount) {{
                alert('Payment amount must be at least $99.00');
                return false;
            }}
            return true;
        }}
        
        document.getElementById('amount').addEventListener('input', function() {{
            const btn = document.getElementById('payBtn');
            btn.textContent = 'Pay  + parseFloat(this.value || 0).toFixed(2);
        }});
    </script>
</body>
</html>
"""

@app.route("/process-payment", methods=["POST"])
def process_payment():
    if not session.get("logged_in"):
        return redirect(url_for("index"))
    
    amount = request.form.get("amount", 0)
    
    try:
        amount = float(amount)
    except:
        amount = 0
    
    balance = session.get("balance", 0.00)
    
    if balance >= amount:
        session["vault_unlocked"] = True
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Successful - PaySecure</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f8f9fa;
            color: #1a1a1a;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .success-container {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 48px 32px;
            text-align: center;
            max-width: 420px;
            width: 100%;
        }}
        .checkmark {{
            width: 64px;
            height: 64px;
            background: #d1fae5;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px;
            font-size: 32px;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 32px;
        }}
        .receipt {{
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
            text-align: left;
        }}
        .receipt-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-size: 14px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .receipt-row:last-child {{
            border-bottom: none;
        }}
        .receipt-label {{
            color: #6b7280;
        }}
        .receipt-value {{
            font-weight: 500;
            color: #111827;
        }}
        .receipt-value.green {{
            color: #059669;
        }}
        .btn {{
            display: inline-block;
            padding: 12px 24px;
            background: #3758ff;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            transition: background 0.2s;
        }}
        .btn:hover {{
            background: #2a46d0;
        }}
    </style>
</head>
<body>
    <div class="success-container">
        <div class="checkmark">✓</div>
        <h1>Payment Successful</h1>
        <p class="subtitle">Your transaction has been processed</p>
        
        <div class="receipt">
            <div class="receipt-row">
                <span class="receipt-label">Item</span>
                <span class="receipt-value">Premium Vault Access</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Amount Paid</span>
                <span class="receipt-value green">${amount:.2f}</span>
            </div>
            <div class="receipt-row">
                <span class="receipt-label">Status</span>
                <span class="receipt-value green">Completed</span>
            </div>
        </div>
        
        <a href="/dashboard" class="btn">Go to Dashboard</a>
    </div>
</body>
</html>
"""
    
    else:
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Failed - PaySecure</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #f8f9fa;
            color: #1a1a1a;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .error-container {{
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 48px 32px;
            text-align: center;
            max-width: 420px;
            width: 100%;
        }}
        .error-icon {{
            width: 64px;
            height: 64px;
            background: #fee2e2;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 24px;
            font-size: 32px;
            color: #dc2626;
        }}
        h1 {{
            font-size: 24px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 8px;
        }}
        .subtitle {{
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 32px;
            line-height: 1.5;
        }}
        .details {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
            text-align: left;
        }}
        .details-row {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            font-size: 14px;
            border-bottom: 1px solid #fecaca;
        }}
        .details-row:last-child {{
            border-bottom: none;
        }}
        .details-label {{
            color: #6b7280;
        }}
        .details-value {{
            font-weight: 500;
            color: #111827;
        }}
        .details-value.red {{
            color: #dc2626;
        }}
        .btn {{
            display: inline-block;
            padding: 12px 24px;
            background: #3758ff;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            transition: background 0.2s;
        }}
        .btn:hover {{
            background: #2a46d0;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">×</div>
        <h1>Payment Failed</h1>
        <p class="subtitle">Insufficient funds in your account to complete this transaction</p>
        
        <div class="details">
            <div class="details-row">
                <span class="details-label">Your Balance</span>
                <span class="details-value red">${balance:.2f}</span>
            </div>
            <div class="details-row">
                <span class="details-label">Amount Required</span>
                <span class="details-value">${amount:.2f}</span>
            </div>
            <div class="details-row">
                <span class="details-label">Shortfall</span>
                <span class="details-value red">-${(amount - balance):.2f}</span>
            </div>
        </div>
        
        <a href="/payment" class="btn">Try Again</a>
    </div>
</body>
</html>
"""

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/success")
def success():
    return redirect("/dashboard")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)