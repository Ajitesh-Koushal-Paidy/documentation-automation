# Using This Repository

This repository is **open source** and can be used by anyone to automate their Confluence documentation!

## 🎯 Who Can Use This?

✅ **Anyone with:**
- Confluence pages to maintain
- Jira for issue tracking
- Sentry for error monitoring (optional)
- Python 3.9+

## 🚀 Quick Start for New Users

### Step 1: Clone Repository

```bash
git clone https://github.com/Ajitesh-Koushal-Paidy/documentation-automation.git
cd documentation-automation
```

### Step 2: Install Dependencies

```bash
pip install requests
```

### Step 3: Configure for Your Organization

#### Get Your API Tokens

**Confluence/Jira Token:**
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Create new token
3. Save it securely

**Sentry Token (optional):**
1. Go to: https://sentry.io/settings/account/api/auth-tokens/
2. Create token with `project:read`, `event:read`, `org:read`

#### Create Configuration

```bash
cp config/config.template.json config/config.json
```

Edit `config/config.json`:

```json
{
  "confluence": {
    "url": "https://YOUR-DOMAIN.atlassian.net",
    "email": "your.email@company.com",
    "token": "YOUR_CONFLUENCE_TOKEN"
  },
  "pages": {
    "page1": {
      "id": "YOUR_PAGE_ID",
      "name": "Your Documentation Page"
    }
  }
}
```

#### Update Script Paths

Edit each script in `scripts/` directory:

```python
# Change these to your paths
REPO_PATH = "/path/to/your/repository"
BASE_DIR = "/path/to/your/home"
```

### Step 4: Set Environment Variables

```bash
# Option 1: Export in shell
export CONFLUENCE_API_TOKEN="your-token-here"
export FIGMA_TOKEN="your-figma-token-here"

# Option 2: Create .env file (recommended)
cat > .env << EOF
CONFLUENCE_API_TOKEN=your-token-here
FIGMA_TOKEN=your-figma-token-here
EOF
```

### Step 5: Test

```bash
# Test Mobile App automation (customize first)
python3 scripts/auto-update-confluence.py

# Test Checkout automation (customize first)
python3 scripts/auto-update-checkout-confluence.py

# Test PAECS automation (customize first)
python3 scripts/auto-update-paecs-confluence.py
```

## 📝 Customization Guide

### For Different Documentation Types

#### Basic Confluence Page Updates

Use `auto-update-paecs-confluence.py` as template:
- Just updates "Last Updated" date
- Minimal configuration needed
- Works with any Confluence page

#### Documentation with Git Monitoring

Use `auto-update-confluence.py` as template:
- Monitors git repository for changes
- Tracks specific files/directories
- Updates based on code changes

#### Documentation with File Monitoring

Use `auto-update-checkout-confluence.py` as template:
- Monitors markdown/documentation files
- MD5 hash-based change detection
- No git dependency

### Modify for Your Use Case

**1. Change Page IDs:**

In each script, update:
```python
PAGE_ID = "YOUR_CONFLUENCE_PAGE_ID"
```

Find your page ID from the URL:
```
https://your-domain.atlassian.net/wiki/spaces/XXX/pages/1234567/Page+Title
                                                              ^^^^^^^ This is your Page ID
```

**2. Change Monitoring Paths:**

Update paths to match your setup:
```python
REPO_PATH = "/your/path/to/repository"
BASE_DIR = "/your/base/directory"
```

**3. Customize Content:**

Modify the content generation functions to match your documentation structure.

## 🤖 Claude Agent (Optional)

If you use Claude Code, install the agent:

```bash
mkdir -p ~/.claude/agents
cp claude-agent/doc-automation-agent.md ~/.claude/agents/
```

Then use with:
```
@doc-automation check status
```

## 📅 Automation Setup

### Cron Jobs

```bash
crontab -e
```

Add (customize paths):
```bash
# Weekly documentation updates (every Monday 9 AM)
0 9 * * 1 cd /path/to/documentation-automation && python3 scripts/auto-update-confluence.py >> logs/cron.log 2>&1
```

### GitHub Actions

Create `.github/workflows/update-docs.yml`:

```yaml
name: Update Documentation

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday 9 AM
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install requests
      - name: Update documentation
        env:
          CONFLUENCE_API_TOKEN: ${{ secrets.CONFLUENCE_API_TOKEN }}
        run: python3 scripts/auto-update-confluence.py
```

Add secrets in GitHub: Settings → Secrets → Actions

## 🔐 Security Best Practices

### Never Commit:
- ❌ API tokens
- ❌ `config/config.json` (with real tokens)
- ❌ `.env` files
- ❌ Log files with sensitive data

### Always:
- ✅ Use environment variables
- ✅ Use `.gitignore` (already configured)
- ✅ Rotate tokens regularly
- ✅ Use minimum required permissions

## 🎨 Customization Examples

### Example 1: Single Confluence Page

Simplest use case - just update date on one page:

```python
import requests
import os
from datetime import datetime

CONFLUENCE_URL = "https://your-domain.atlassian.net"
PAGE_ID = "your-page-id"
EMAIL = "your-email@company.com"
TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

# Get page, update date, push back
# See auto-update-paecs-confluence.py for full example
```

### Example 2: Multiple Pages

Monitor multiple pages:

```python
PAGES = {
    'docs': '123456',
    'api': '789012',
    'guide': '345678'
}

for name, page_id in PAGES.items():
    update_page(page_id)
```

### Example 3: Different Content Types

Adapt for your content:

```python
# For API documentation
def update_api_docs():
    # Parse OpenAPI specs
    # Update Confluence
    pass

# For release notes
def update_release_notes():
    # Get latest git tags
    # Format changelog
    # Update Confluence
    pass
```

## 📖 Documentation Structure

### What's Included:
- `README.md` - Overview and features
- `docs/SETUP.md` - Detailed setup guide
- `GITHUB_SETUP.md` - GitHub publishing guide
- This file - Usage for others

### Scripts:
- `auto-update-confluence.py` - Mobile app docs (complex example)
- `auto-update-checkout-confluence.py` - File monitoring (medium)
- `auto-update-paecs-confluence.py` - Simple date update (simple)
- `doc-health-check.py` - Health monitoring

Choose the script that matches your complexity level!

## 💡 Tips for Success

1. **Start Simple:** Begin with `auto-update-paecs-confluence.py`
2. **Test Locally:** Run manually before scheduling
3. **Check Logs:** Monitor first few runs
4. **Iterate:** Add features as needed
5. **Document:** Update README with your customizations

## 🆘 Getting Help

- **Issues:** Open issue on GitHub
- **Documentation:** See `/docs` folder
- **Examples:** See existing scripts
- **Community:** Fork and share improvements!

## 📜 License

MIT License - See LICENSE file

You can:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

You must:
- Include copyright notice
- Include license

## 🤝 Contributing

Contributions welcome!

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit Pull Request

## 🎯 Common Use Cases

### For Documentation Teams:
- Automate weekly doc reviews
- Keep "Last Updated" dates current
- Monitor doc coverage

### For Engineering Teams:
- Auto-update API docs from code
- Sync release notes
- Track documentation health

### For Support Teams:
- Keep handbooks current
- Auto-update FAQs
- Monitor documentation staleness

## ✅ Success Stories

This system currently manages:
- 3 Confluence pages
- 32 documented screens
- 94.8% documentation health score
- Zero manual maintenance

You can achieve similar results!

## 📞 Support

- **GitHub Issues:** Report bugs or request features
- **Discussions:** Ask questions, share ideas
- **Wiki:** Community documentation

---

**This repository is open source and free to use. Customize it for your needs!** 🚀

## Quick Links

- [Main README](../README.md)
- [Setup Guide](../docs/SETUP.md)
- [GitHub Setup](../GITHUB_SETUP.md)
- [License](../LICENSE)
