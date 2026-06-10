# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing the maintainer directly. **Do not** create a public GitHub issue for security vulnerabilities.

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and aim to release a fix within 7 days for critical issues.

---

## Security Best Practices

### 1. API Token Management

**✅ DO:**
- Store API tokens in environment variables
- Use the configuration file (`config/config.json`) with proper permissions (chmod 600)
- Rotate tokens regularly (every 90 days)
- Use separate tokens for different environments (dev, staging, production)

**❌ DON'T:**
- Commit tokens to git
- Share tokens in plain text (Slack, email, etc.)
- Use production tokens in development
- Log API tokens in application logs

### 2. Configuration Security

**Protecting `config/config.json`:**

```bash
# Set proper file permissions
chmod 600 config/config.json

# Verify it's in .gitignore
git check-ignore config/config.json
```

**Using Environment Variables:**

```bash
# Set via environment
export CONFLUENCE_API_TOKEN="your-token-here"
export CONFLUENCE_EMAIL="your@email.com"

# Or use .env file (never commit it!)
echo "CONFLUENCE_API_TOKEN=your-token" >> .env
```

### 3. Repository Security

**Before Pushing to GitHub:**

```bash
# Check for secrets
git diff --cached | grep -E "token|password|secret|key"

# Use git-secrets (recommended)
git secrets --scan

# Use gitleaks
gitleaks detect --source . --verbose
```

**If You Accidentally Commit a Secret:**

1. **IMMEDIATELY** rotate the exposed credential
2. Remove from git history:
   ```bash
   # Install git-filter-repo
   pip3 install git-filter-repo
   
   # Replace secret in all commits
   git-filter-repo --replace-text <(echo "SECRET_VALUE==>***REMOVED***") --force
   
   # Force push
   git push --force origin main
   ```
3. Verify it's gone: `git log --all --grep="SECRET"`

### 4. Secure Script Execution

**Command Injection Prevention:**

```python
# ❌ VULNERABLE
cmd = f"git log --since='{user_input}'"
subprocess.run(cmd, shell=True)

# ✅ SECURE
subprocess.run(['git', 'log', f'--since={user_input}'], cwd=repo_path)
```

**File Path Validation:**

```python
# Always validate and sanitize file paths
from pathlib import Path

def safe_path(base_dir, user_path):
    """Ensure path is within base directory"""
    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()
    if not target.is_relative_to(base):
        raise ValueError("Path traversal attempt detected")
    return target
```

### 5. API Request Security

**Rate Limiting:**

```python
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    """Decorator to rate limit API calls"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

**Timeout Configuration:**

```python
import requests

# Always set timeouts
response = requests.get(url, auth=auth, timeout=30)
```

### 6. Logging Security

**Safe Logging:**

```python
import logging
import re

def sanitize_log(message):
    """Remove sensitive data from logs"""
    # Redact tokens
    message = re.sub(r'(token|password|key)=[^\s&]+', r'\1=***REDACTED***', message)
    # Redact email
    message = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', message)
    return message

# Use it
logging.info(sanitize_log(f"Request to {url}"))
```

### 7. Dependency Security

**Keep Dependencies Updated:**

```bash
# Check for vulnerabilities
pip-audit

# Update dependencies
pip install --upgrade requests

# Pin versions in requirements.txt
requests==2.31.0
```

### 8. Access Control

**File Permissions:**

```bash
# Scripts should not be world-writable
chmod 755 scripts/*.py

# Config files should be private
chmod 600 config/config.json

# Log files should be readable by owner only
chmod 600 logs/*.log
```

**Cron Job Security:**

```bash
# Use full paths in cron
0 9 * * 1 /usr/bin/python3 /full/path/to/script.py

# Never run as root unless absolutely necessary
# Use dedicated service account

# Limit environment variables
0 9 * * 1 env -i HOME=/home/user /usr/bin/python3 script.py
```

### 9. Input Validation

**Always Validate:**

```python
def validate_page_id(page_id):
    """Validate Confluence page ID"""
    if not isinstance(page_id, str):
        raise ValueError("Page ID must be string")
    if not page_id.isdigit():
        raise ValueError("Page ID must be numeric")
    if len(page_id) > 20:
        raise ValueError("Page ID too long")
    return page_id
```

### 10. Secure Development Checklist

**Before Every Commit:**

- [ ] No secrets in code
- [ ] No hardcoded credentials
- [ ] No personal information (email, paths)
- [ ] Input validation implemented
- [ ] Error messages don't expose sensitive data
- [ ] Using `subprocess` safely (no `shell=True` with user input)
- [ ] API tokens from environment/config only
- [ ] File permissions checked
- [ ] Dependencies up to date

**Before Every Release:**

- [ ] Security scan completed
- [ ] Dependencies audited
- [ ] Documentation reviewed
- [ ] Test credentials removed
- [ ] Production config template updated
- [ ] CHANGELOG.md updated
- [ ] Git tags signed

---

## Security Audit Log

### 2026-06-10: Initial Security Audit

**Issues Found:**
1. ✅ FIXED: Hardcoded API token in `claude-agent/doc-automation-agent.md`
2. ✅ FIXED: Command injection vulnerability via `shell=True`
3. ✅ FIXED: Hardcoded personal paths in Python scripts
4. ✅ FIXED: Hardcoded company information in scripts

**Actions Taken:**
- Removed token from git history using `git-filter-repo`
- Replaced `shell=True` subprocess calls with list-based calls
- Created `config_loader.py` for centralized configuration
- Updated all scripts to use configuration loader
- Added comprehensive security documentation

**Recommendations:**
- Rotate exposed Confluence API token immediately
- Enable branch protection on GitHub
- Add pre-commit hooks for secret detection
- Set up automated security scanning

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Git Secrets Tool](https://github.com/awslabs/git-secrets)
- [Gitleaks Scanner](https://github.com/gitleaks/gitleaks)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

## Contact

For security concerns, contact the repository maintainer directly.

**Last Updated:** June 10, 2026
