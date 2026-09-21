# Al-La'eeb Security Policy

## Authentication
- JWT tokens with 30-minute expiry
- Refresh tokens with 7-day expiry, single-use
- Passwords: minimum 10 characters, uppercase, number, special char
- Bcrypt with 12 rounds
- Brute-force protection: 5 attempts per IP, 15-minute lockout
- Token blacklisting on logout

## Authorization
- Role-Based Access Control (RBAC)
- Resource-level permissions
- API rate limiting: 60 req/min per IP, 120 per user

## Data Protection
- TLS 1.3 for all communications
- Database encryption at rest
- Biometric data encrypted with AES-256
- PII anonymization in logs

## Infrastructure
- Docker containers run as non-root
- Read-only filesystems where possible
- No new privileges
- Network isolation
- Security headers on all responses

## Compliance
- Audit logging for all auth events
- 90-day log retention
- GDPR-compliant data handling
- Biometric data consent required
