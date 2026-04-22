# Security Checklist

> **Mục đích**: Security audit & vulnerability assessment theo OWASP Top 10

---

## 🎯 Security Goals

| Area | Status | Notes |
|------|--------|-------|
| **OWASP Top 10** | ⬜ Pass | ___ |
| **Penetration Testing** | ⬜ Pass | ___ |
| **Dependency Audit** | ⬜ Pass | ___ |
| **SSL/TLS** | ⬜ A+ Rating | ___ |
| **Security Headers** | ⬜ Configured | ___ |

---

## 🔒 OWASP Top 10 (2021)

### A01: Broken Access Control
- [ ] Implement proper authorization checks
- [ ] Validate user permissions on every request
- [ ] Prevent directory traversal attacks
- [ ] Disable directory listing
- [ ] Implement rate limiting on sensitive endpoints

```javascript
// Authorization middleware
const checkPermission = (requiredRole) => {
  return (req, res, next) => {
    if (!req.user || req.user.role !== requiredRole) {
      return res.status(403).json({ error: 'Forbidden' })
    }
    next()
  }
}

// Usage
app.delete('/api/users/:id', checkPermission('admin'), deleteUser)
```

### A02: Cryptographic Failures
- [ ] Use HTTPS everywhere (enforce with HSTS)
- [ ] Encrypt sensitive data at rest
- [ ] Use strong encryption algorithms (AES-256)
- [ ] Secure password storage (bcrypt, Argon2)
- [ ] Rotate encryption keys regularly

```javascript
// Password hashing with bcrypt
const bcrypt = require('bcrypt')
const saltRounds = 12

const hashedPassword = await bcrypt.hash(password, saltRounds)
```

### A03: Injection
- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Validate & sanitize all user inputs
- [ ] Use ORM/query builders (Prisma, TypeORM)
- [ ] Escape output in templates (prevent XSS)
- [ ] Use Content Security Policy (CSP)

```javascript
// SQL injection prevention with parameterized query
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
)

// XSS prevention with DOMPurify
import DOMPurify from 'dompurify'
const clean = DOMPurify.sanitize(userInput)
```

### A04: Insecure Design
- [ ] Implement threat modeling
- [ ] Use secure design patterns
- [ ] Principle of least privilege
- [ ] Defense in depth
- [ ] Fail securely (default deny)

### A05: Security Misconfiguration
- [ ] Remove default credentials
- [ ] Disable unnecessary features
- [ ] Keep software up to date
- [ ] Configure security headers
- [ ] Remove debug/verbose error messages in production

```javascript
// Security headers with Helmet.js
const helmet = require('helmet')

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}))
```

### A06: Vulnerable and Outdated Components
- [ ] Audit dependencies regularly (npm audit)
- [ ] Update dependencies to latest secure versions
- [ ] Remove unused dependencies
- [ ] Use Dependabot/Renovate for automated updates
- [ ] Monitor CVE databases

```bash
# Audit dependencies
npm audit
npm audit fix

# Check for outdated packages
npm outdated

# Use Snyk for vulnerability scanning
npx snyk test
```

### A07: Identification and Authentication Failures
- [ ] Implement multi-factor authentication (MFA)
- [ ] Use strong password policies
- [ ] Implement account lockout after failed attempts
- [ ] Secure session management
- [ ] Use secure, httpOnly, sameSite cookies

```javascript
// Secure cookie configuration
res.cookie('sessionId', token, {
  httpOnly: true,
  secure: true, // HTTPS only
  sameSite: 'strict',
  maxAge: 3600000, // 1 hour
})

// Rate limiting for login attempts
const rateLimit = require('express-rate-limit')

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
})

app.post('/api/login', loginLimiter, login)
```

### A08: Software and Data Integrity Failures
- [ ] Use Subresource Integrity (SRI) for CDN resources
- [ ] Verify digital signatures
- [ ] Implement CI/CD pipeline security
- [ ] Use code signing
- [ ] Verify package integrity (lock files)

```html
<!-- Subresource Integrity for CDN -->
<script 
  src="https://cdn.example.com/library.js"
  integrity="sha384-oqVuAfXRKap7fdgcCY5uykM6+R9GqQ8K/ux..."
  crossorigin="anonymous">
</script>
```

### A09: Security Logging and Monitoring Failures
- [ ] Log all authentication attempts
- [ ] Log authorization failures
- [ ] Monitor for suspicious activity
- [ ] Set up alerts for security events
- [ ] Implement centralized logging

```javascript
// Security event logging
const logger = require('winston')

logger.info('User login', { userId, ip, timestamp })
logger.warn('Failed login attempt', { email, ip, timestamp })
logger.error('Unauthorized access attempt', { userId, resource, timestamp })
```

### A10: Server-Side Request Forgery (SSRF)
- [ ] Validate & sanitize URLs
- [ ] Use allowlist for external requests
- [ ] Disable unnecessary protocols (file://, gopher://)
- [ ] Implement network segmentation
- [ ] Use firewall rules

```javascript
// URL validation to prevent SSRF
const isValidUrl = (url) => {
  const allowedDomains = ['api.example.com', 'cdn.example.com']
  const parsed = new URL(url)
  return allowedDomains.includes(parsed.hostname)
}

if (!isValidUrl(userProvidedUrl)) {
  throw new Error('Invalid URL')
}
```

---

## 🔐 Authentication & Authorization

### Password Security
- [ ] Minimum 8 characters
- [ ] Require uppercase, lowercase, number, special char
- [ ] Implement password strength meter
- [ ] Prevent common passwords (top 10k list)
- [ ] Hash passwords with bcrypt/Argon2 (cost factor 12+)

### Session Management
- [ ] Generate cryptographically random session IDs
- [ ] Regenerate session ID after login
- [ ] Implement session timeout (30 min idle)
- [ ] Secure logout (invalidate session)
- [ ] Use httpOnly, secure, sameSite cookies

### JWT Security
- [ ] Use strong secret key (256-bit+)
- [ ] Set short expiration time (15 min)
- [ ] Implement refresh tokens
- [ ] Validate JWT signature
- [ ] Store JWT securely (not in localStorage)

```javascript
// JWT configuration
const jwt = require('jsonwebtoken')

const accessToken = jwt.sign(
  { userId: user.id },
  process.env.JWT_SECRET,
  { expiresIn: '15m' }
)

const refreshToken = jwt.sign(
  { userId: user.id },
  process.env.JWT_REFRESH_SECRET,
  { expiresIn: '7d' }
)
```

---

## 🌐 Network Security

### HTTPS/TLS
- [ ] Force HTTPS (redirect HTTP to HTTPS)
- [ ] Use TLS 1.3 (disable TLS 1.0, 1.1)
- [ ] Use strong cipher suites
- [ ] Implement HSTS (HTTP Strict Transport Security)
- [ ] Get A+ rating on SSL Labs

```nginx
# Nginx HTTPS configuration
server {
  listen 443 ssl http2;
  ssl_certificate /path/to/cert.pem;
  ssl_certificate_key /path/to/key.pem;
  ssl_protocols TLSv1.3 TLSv1.2;
  ssl_ciphers HIGH:!aNULL:!MD5;
  
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
}
```

### Security Headers
- [ ] Content-Security-Policy (CSP)
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY
- [ ] X-XSS-Protection: 1; mode=block
- [ ] Referrer-Policy: strict-origin-when-cross-origin
- [ ] Permissions-Policy

```javascript
// Security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff')
  res.setHeader('X-Frame-Options', 'DENY')
  res.setHeader('X-XSS-Protection', '1; mode=block')
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin')
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')
  next()
})
```

### CORS Configuration
- [ ] Whitelist allowed origins (no wildcard *)
- [ ] Restrict allowed methods
- [ ] Restrict allowed headers
- [ ] Set credentials: true only when needed

```javascript
// CORS configuration
const cors = require('cors')

app.use(cors({
  origin: ['https://example.com', 'https://www.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
}))
```

---

## 🛡️ Input Validation & Sanitization

### Validation Rules
- [ ] Validate all user inputs (client & server)
- [ ] Use schema validation (Zod, Joi, Yup)
- [ ] Whitelist allowed characters
- [ ] Validate data types & formats
- [ ] Validate file uploads (type, size, content)

```javascript
// Input validation with Zod
const { z } = require('zod')

const userSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  age: z.number().int().min(18).max(120),
})

const result = userSchema.safeParse(req.body)
if (!result.success) {
  return res.status(400).json({ errors: result.error.errors })
}
```

### File Upload Security
- [ ] Validate file type (MIME type & extension)
- [ ] Limit file size (max 10MB)
- [ ] Scan for malware (ClamAV)
- [ ] Store files outside web root
- [ ] Generate random filenames

```javascript
// File upload validation
const multer = require('multer')

const upload = multer({
  limits: { fileSize: 10 * 1024 * 1024 }, // 10MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
    if (!allowedTypes.includes(file.mimetype)) {
      return cb(new Error('Invalid file type'))
    }
    cb(null, true)
  },
})
```

---

## 🧪 Penetration Testing

### Automated Scanning
- [ ] OWASP ZAP (Zed Attack Proxy)
- [ ] Burp Suite Community Edition
- [ ] Nikto web scanner
- [ ] SQLMap (SQL injection testing)
- [ ] XSStrike (XSS testing)

```bash
# OWASP ZAP baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://your-site.com \
  -r zap-report.html
```

### Manual Testing
- [ ] Test authentication bypass
- [ ] Test authorization bypass
- [ ] Test SQL injection
- [ ] Test XSS (reflected, stored, DOM-based)
- [ ] Test CSRF
- [ ] Test file upload vulnerabilities
- [ ] Test business logic flaws

---

## 📦 Dependency Security

### Audit Tools
```bash
# npm audit
npm audit
npm audit fix

# Snyk
npx snyk test
npx snyk monitor

# OWASP Dependency-Check
dependency-check --project "MyProject" --scan .
```

### Checklist
- [ ] Run npm audit weekly
- [ ] Update dependencies monthly
- [ ] Remove unused dependencies
- [ ] Use lock files (package-lock.json)
- [ ] Monitor security advisories

---

## 🔍 Security Monitoring

### Logging
- [ ] Log authentication events
- [ ] Log authorization failures
- [ ] Log input validation failures
- [ ] Log rate limit violations
- [ ] Log suspicious activity

### Alerts
- [ ] Alert on multiple failed login attempts
- [ ] Alert on privilege escalation attempts
- [ ] Alert on unusual traffic patterns
- [ ] Alert on critical vulnerabilities

### Tools
- [ ] Sentry (error tracking)
- [ ] Datadog (monitoring)
- [ ] CloudFlare (DDoS protection)
- [ ] AWS GuardDuty (threat detection)

---

## ✅ Pre-Launch Security Checklist

### Infrastructure
- [ ] HTTPS enabled with valid certificate
- [ ] Security headers configured
- [ ] CORS configured correctly
- [ ] Rate limiting enabled
- [ ] Firewall rules configured
- [ ] DDoS protection enabled

### Application
- [ ] All OWASP Top 10 vulnerabilities addressed
- [ ] Input validation implemented
- [ ] Authentication & authorization secure
- [ ] Sensitive data encrypted
- [ ] Error messages sanitized (no stack traces)
- [ ] Debug mode disabled in production

### Dependencies
- [ ] npm audit passed (0 vulnerabilities)
- [ ] All dependencies up to date
- [ ] No known CVEs in dependencies

### Testing
- [ ] Penetration testing completed
- [ ] Security scan passed (OWASP ZAP)
- [ ] Code review completed
- [ ] Security audit signed off

---

## 🔗 Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [Security Headers](https://securityheaders.com/)
