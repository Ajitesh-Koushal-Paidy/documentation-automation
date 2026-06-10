# Setup Guide

Complete setup guide for the Documentation Automation System.

## Prerequisites

- Python 3.9 or higher
- Git
- Access to Confluence (API token)
- Access to Jira (API token)
- Unix/Linux/macOS with cron
- Node.js 14+ (for Sentry-Jira automation)

## Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/documentation-automation.git
cd documentation-automation
```

## Step 2: Install Dependencies

### Python Dependencies
```bash
pip install requests
```

### Node Dependencies (for Sentry-Jira)
```bash
cd sentry-jira
npm install
cd ..
```

## Step 3: Generate API Tokens

### Confluence/Jira API Token

1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Name it: "Documentation Automation"
4. Copy the token (save it securely)

### Sentry API Token

1. Go to: https://sentry.io/settings/account/api/auth-tokens/
2. Click "Create New Token"
3. Scopes needed:
   - `project:read`
   - `event:read`
   - `org:read`
4. Copy the token

## Step 4: Configure

```bash
cp config/config.template.json config/config.json
```

Edit `config/config.json`:

```json
{
  "confluence": {
    "url": "https://paidy-portal.atlassian.net",
    "email": "your.email@paidy.com",
    "token": "YOUR_ACTUAL_TOKEN_HERE"
  },
  "pages": {
    "mobileApp": {
      "id": "5015076940",
      "name": "Mobile App Documentation",
      "repoPath": "/Users/username/workspace/paidy-app-rn"
    },
    "checkout": {
      "id": "5015404871",
      "name": "Checkout Documentation",
      "docsPath": "/Users/username"
    },
    "paecs": {
      "id": "3223651657",
      "name": "PAECS Handbook"
    }
  },
  "sentry": {
    "org": "paidy",
    "project": "paidy-app-rn",
    "token": "YOUR_SENTRY_TOKEN_HERE"
  }
}
```

⚠️ **Important:** Never commit `config/config.json` to git!

## Step 5: Update Script Paths

Edit each script in `scripts/` to use your paths:

```python
# In auto-update-confluence.py
REPO_PATH = "/Users/YOUR_USERNAME/workspace/paidy-app-rn"
BASE_DIR = "/Users/YOUR_USERNAME"
```

## Step 6: Test Scripts

```bash
# Test Mobile App automation
python3 scripts/auto-update-confluence.py

# Test Checkout automation
python3 scripts/auto-update-checkout-confluence.py

# Test PAECS automation
python3 scripts/auto-update-paecs-confluence.py

# Test health check
python3 scripts/doc-health-check.py
```

## Step 7: Setup Cron Jobs

```bash
crontab -e
```

Add these lines:

```bash
# Documentation updates (every Monday 9 AM)
0 9 * * 1 cd /path/to/documentation-automation && python3 scripts/auto-update-confluence.py >> logs/auto-update-cron.log 2>&1
0 9 * * 1 cd /path/to/documentation-automation && python3 scripts/auto-update-checkout-confluence.py >> logs/auto-update-checkout-cron.log 2>&1
0 9 * * 1 cd /path/to/documentation-automation && python3 scripts/auto-update-paecs-confluence.py >> logs/auto-update-paecs-cron.log 2>&1

# Sentry-Jira automation (daily 9:03 AM)
3 9 * * * cd /path/to/documentation-automation/sentry-jira && node run-automation.js >> ../logs/sentry-jira-cron.log 2>&1
```

## Step 8: Setup Claude Agent

Copy agent to Claude Code:

```bash
mkdir -p ~/.claude/agents
cp claude-agent/doc-automation-agent.md ~/.claude/agents/
```

Test the agent:
```
@doc-automation check status
```

## Step 9: Verify Installation

```bash
# Check cron jobs
crontab -l

# Check scripts are executable
ls -l scripts/*.py

# Check config exists
ls -l config/config.json

# Test API connection
python3 << 'EOF'
import requests
import json

with open('config/config.json') as f:
    config = json.load(f)

r = requests.get(
    f"{config['confluence']['url']}/wiki/rest/api/user/current",
    auth=(config['confluence']['email'], config['confluence']['token'])
)
print(f"API Status: {r.status_code}")
if r.status_code == 200:
    print(f"✅ Connected as: {r.json()['displayName']}")
else:
    print(f"❌ Error: {r.json()}")
EOF
```

## Step 10: First Run

```bash
# Manual run to initialize
python3 scripts/auto-update-confluence.py
python3 scripts/auto-update-checkout-confluence.py
python3 scripts/auto-update-paecs-confluence.py

# Check logs
tail logs/*.txt
```

## Troubleshooting

### Issue: API Authentication Failed

**Solution:**
1. Verify token is correct
2. Check email matches your Atlassian account
3. Regenerate token if needed

### Issue: Module Not Found

**Solution:**
```bash
pip install requests
```

### Issue: Cron Jobs Not Running

**Solution:**
1. Check cron service: `sudo systemctl status cron` (Linux) or `ps aux | grep cron` (macOS)
2. Check paths are absolute in crontab
3. Check logs: `tail logs/*-cron.log`

### Issue: Permission Denied

**Solution:**
```bash
chmod +x scripts/*.py
```

## Next Steps

1. Monitor logs for first week
2. Verify updates are working
3. Check Confluence pages are updating
4. Setup Slack notifications (optional)
5. Add monitoring dashboard (optional)

## Security Best Practices

1. ✅ Never commit API tokens
2. ✅ Use `.gitignore` for sensitive files
3. ✅ Rotate tokens every 90 days
4. ✅ Use separate tokens for dev/prod
5. ✅ Limit token scopes to minimum required
6. ✅ Monitor logs for suspicious activity

## Support

- **Documentation:** [README.md](../README.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Issues:** GitHub Issues

---

**Setup complete! Your documentation automation is ready.** 🎉
