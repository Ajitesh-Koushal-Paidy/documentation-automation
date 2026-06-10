# Quick Start Guide - Running the Automation

## Prerequisites

- ✅ Python 3.9+
- ✅ Git repository access
- ✅ Confluence API token (rotate the old one!)
- ✅ Unix/Linux/macOS environment

---

## Setup (One-Time)

### Step 1: Create Configuration File

```bash
cd /Users/ajitesh.koushal/projects/documentation-automation

# Copy the template
cp config/config.template.json config/config.json

# Set proper permissions
chmod 600 config/config.json
```

### Step 2: Edit Configuration

Open `config/config.json` and fill in your values:

```json
{
  "paths": {
    "baseDir": "/Users/ajitesh.koushal",
    "repoPath": "/Users/ajitesh.koushal/Desktop/paidy-app-rn",
    "screenshotsDir": "/Users/ajitesh.koushal/figma-screenshots-individual",
    "docsPath": "/Users/ajitesh.koushal"
  },
  "confluence": {
    "url": "https://paidy-portal.atlassian.net",
    "email": "ajitesh.koushal@paidy.com",
    "token": "YOUR_NEW_CONFLUENCE_API_TOKEN_HERE"
  },
  "pages": {
    "mobileApp": {
      "id": "5015076940",
      "name": "Mobile App Documentation"
    },
    "checkout": {
      "id": "5015404871",
      "name": "Checkout Documentation"
    },
    "paecs": {
      "id": "3223651657",
      "name": "PAECS Handbook"
    }
  },
  "figma": {
    "token": "YOUR_FIGMA_TOKEN_HERE",
    "fileKeys": [
      "N9udhE5uXkpWbeFqANlCKt",
      "fMTt9gNfuq9yt0e9XFKEpJ"
    ]
  }
}
```

**IMPORTANT:** Get a new Confluence token at:  
👉 https://id.atlassian.com/manage-profile/security/api-tokens

---

## Running the Scripts

### Manual Execution

```bash
cd /Users/ajitesh.koushal/projects/documentation-automation

# Update Mobile App documentation
python3 scripts/auto-update-confluence.py

# Update Checkout documentation
python3 scripts/auto-update-checkout-confluence.py

# Update PAECS Handbook
python3 scripts/auto-update-paecs-confluence.py

# Check documentation health
python3 scripts/doc-health-check.py
```

### Run All at Once

```bash
cd /Users/ajitesh.koushal/projects/documentation-automation

# Update all three pages
python3 scripts/auto-update-confluence.py && \
python3 scripts/auto-update-checkout-confluence.py && \
python3 scripts/auto-update-paecs-confluence.py

# Check results
echo "✅ All updates complete!"
```

### View Logs

```bash
# View recent activity
tail -50 /Users/ajitesh.koushal/auto-update-log.txt
tail -50 /Users/ajitesh.koushal/auto-update-checkout-log.txt
tail -50 /Users/ajitesh.koushal/auto-update-paecs-log.txt

# Watch live (press Ctrl+C to stop)
tail -f /Users/ajitesh.koushal/auto-update-*.txt

# Check for errors
grep -i "error\|failed" /Users/ajitesh.koushal/auto-update-*.txt
```

---

## Using Environment Variables (Alternative)

If you prefer not to create a config file, use environment variables:

### Temporary (Current Session Only)

```bash
export CONFLUENCE_API_TOKEN="your-token-here"
export CONFLUENCE_EMAIL="ajitesh.koushal@paidy.com"
export CONFLUENCE_URL="https://paidy-portal.atlassian.net"
export BASE_DIR="/Users/ajitesh.koushal"
export REPO_PATH="/Users/ajitesh.koushal/Desktop/paidy-app-rn"
export MOBILE_APP_PAGE_ID="5015076940"
export CHECKOUT_PAGE_ID="5015404871"
export PAECS_PAGE_ID="3223651657"
export FIGMA_TOKEN="your-figma-token"

# Now run the scripts
python3 scripts/auto-update-confluence.py
```

### Permanent (Add to ~/.zshrc)

```bash
# Edit your shell config
nano ~/.zshrc

# Add these lines at the end:
export CONFLUENCE_API_TOKEN="your-token-here"
export CONFLUENCE_EMAIL="ajitesh.koushal@paidy.com"
export CONFLUENCE_URL="https://paidy-portal.atlassian.net"
export BASE_DIR="/Users/ajitesh.koushal"
export REPO_PATH="/Users/ajitesh.koushal/Desktop/paidy-app-rn"
export MOBILE_APP_PAGE_ID="5015076940"
export CHECKOUT_PAGE_ID="5015404871"
export PAECS_PAGE_ID="3223651657"

# Save and reload
source ~/.zshrc

# Test it works
echo $CONFLUENCE_API_TOKEN
```

---

## Setting Up Cron (Automated Runs)

To run automatically every Monday at 9:00 AM:

### Step 1: Create wrapper script

```bash
cat > ~/run-doc-automation.sh << 'EOF'
#!/bin/bash
# Documentation Automation Runner

# Load environment
export CONFLUENCE_API_TOKEN="your-token-here"
export CONFLUENCE_EMAIL="ajitesh.koushal@paidy.com"
export CONFLUENCE_URL="https://paidy-portal.atlassian.net"
export BASE_DIR="/Users/ajitesh.koushal"
export REPO_PATH="/Users/ajitesh.koushal/Desktop/paidy-app-rn"
export MOBILE_APP_PAGE_ID="5015076940"
export CHECKOUT_PAGE_ID="5015404871"
export PAECS_PAGE_ID="3223651657"

cd /Users/ajitesh.koushal/projects/documentation-automation

# Run updates
/usr/local/bin/python3 scripts/auto-update-confluence.py >> /Users/ajitesh.koushal/auto-update-cron.log 2>&1
/usr/local/bin/python3 scripts/auto-update-checkout-confluence.py >> /Users/ajitesh.koushal/auto-update-cron.log 2>&1
/usr/local/bin/python3 scripts/auto-update-paecs-confluence.py >> /Users/ajitesh.koushal/auto-update-cron.log 2>&1

echo "$(date): Documentation automation complete" >> /Users/ajitesh.koushal/auto-update-cron.log
EOF

chmod +x ~/run-doc-automation.sh
```

### Step 2: Add to crontab

```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 9 AM)
0 9 * * 1 /Users/ajitesh.koushal/run-doc-automation.sh

# Save and exit (press Esc, type :wq, press Enter)

# Verify it's scheduled
crontab -l
```

### Step 3: Test the cron job

```bash
# Run manually to test
~/run-doc-automation.sh

# Check the log
tail -50 /Users/ajitesh.koushal/auto-update-cron.log
```

---

## Troubleshooting

### Issue: "Config file not found"

**Solution 1:** Create the config file
```bash
cp config/config.template.json config/config.json
# Edit config.json with your values
```

**Solution 2:** Use environment variables
```bash
export CONFLUENCE_API_TOKEN="your-token"
export BASE_DIR="/Users/ajitesh.koushal"
```

### Issue: "CONFLUENCE_API_TOKEN not set"

```bash
# Check if token is set
echo $CONFLUENCE_API_TOKEN

# If empty, set it:
export CONFLUENCE_API_TOKEN="your-token-here"

# Or add to config.json
```

### Issue: "Permission denied"

```bash
# Make scripts executable
chmod +x scripts/*.py

# Check config file permissions
ls -la config/config.json
chmod 600 config/config.json
```

### Issue: "Module 'requests' not found"

```bash
# Install required dependencies
pip3 install requests
```

### Issue: "Repository path not found"

```bash
# Check the path exists
ls -la /Users/ajitesh.koushal/Desktop/paidy-app-rn

# Update in config.json or set environment variable
export REPO_PATH="/correct/path/to/repo"
```

### Issue: "API authentication failed"

**Check token is valid:**
```bash
# Test Confluence API
curl -u "ajitesh.koushal@paidy.com:YOUR_TOKEN" \
  "https://paidy-portal.atlassian.net/wiki/rest/api/user/current"

# Should return your user info
```

If it fails:
1. Token may be expired → Generate new one
2. Token may be revoked → Generate new one
3. Email may be wrong → Update in config

---

## Quick Reference

### Common Commands

```bash
# Run all updates
cd /Users/ajitesh.koushal/projects/documentation-automation
python3 scripts/auto-update-confluence.py
python3 scripts/auto-update-checkout-confluence.py
python3 scripts/auto-update-paecs-confluence.py

# Check health
python3 scripts/doc-health-check.py

# View logs
tail -50 ~/auto-update-log.txt

# Test configuration
python3 -c "from scripts.config_loader import get_config; c = get_config(); print(f'Base: {c.base_dir}, Token: {c.confluence_token[:10]}...')"
```

### File Locations

```
Config:        config/config.json
Scripts:       scripts/*.py
Logs:          ~/auto-update-*.txt  
Data:          ~/screen-*-mapping.json
Screenshots:   ~/figma-screenshots-individual/
```

### Important URLs

- **Confluence API Tokens:** https://id.atlassian.com/manage-profile/security/api-tokens
- **Figma API Tokens:** https://www.figma.com/developers/api#access-tokens
- **Mobile App Page:** https://paidy-portal.atlassian.net/wiki/spaces/UXE/pages/5015076940
- **Checkout Page:** https://paidy-portal.atlassian.net/wiki/spaces/UXE/pages/5015404871
- **PAECS Page:** https://paidy-portal.atlassian.net/wiki/spaces/UXE/pages/3223651657

---

## Next Steps

1. ✅ Create config.json or set environment variables
2. ✅ Get new Confluence API token (rotate the old one!)
3. ✅ Test by running scripts manually
4. ✅ Set up cron job for weekly automation
5. ✅ Monitor logs for first few runs

---

**Questions?** Check `SECURITY.md` for security best practices or `README.md` for full documentation.

**Last Updated:** June 10, 2026
