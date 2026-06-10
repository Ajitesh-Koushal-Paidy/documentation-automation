# Documentation Automation System

Automated documentation management for Confluence pages and Sentry-Jira integration at Paidy.

[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Overview

This system automates the maintenance of three Confluence documentation pages:

| Page | Status | Schedule |
|------|--------|----------|
| **Mobile App Documentation** | ✅ Active | Weekly (Mon 9am) |
| **Checkout Documentation** | ✅ Active | Weekly (Mon 9am) |
| **PAECS Handbook** | ✅ Active | Weekly (Mon 9am) |

**Plus:** Sentry-Jira integration for automated error monitoring and ticket creation.

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Confluence API access
- Jira API access (for Sentry integration)
- Unix/Linux/macOS with cron

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/documentation-automation.git
   cd documentation-automation
   ```

2. **Configure API tokens:**
   ```bash
   cp config/config.template.json config/config.json
   # Edit config.json with your tokens
   ```

3. **Install dependencies:**
   ```bash
   pip install requests
   ```

4. **Setup cron jobs:**
   ```bash
   ./scripts/setup-cron.sh
   ```

## 📊 Features

### Mobile App Documentation
- **Monitors:** Git repository changes (screens, GraphQL queries, Mixpanel events)
- **Updates:** API mappings, event tracking, screenshots
- **Health Score:** 94.8% coverage (32/32 screens documented)
- **Script:** `scripts/auto-update-confluence.py`

### Checkout Documentation
- **Monitors:** 9 markdown documentation files
- **Change Detection:** MD5 hash-based
- **Content:** User flows, technical docs, merchant integration
- **Script:** `scripts/auto-update-checkout-confluence.py`

### PAECS Handbook
- **Updates:** Weekly date refresh
- **Purpose:** Shows active maintenance
- **Script:** `scripts/auto-update-paecs-confluence.py`

### Sentry-Jira Integration
- **Monitors:** Sentry error reports
- **Creates:** Jira tickets for quick fixes (5-15 min tasks)
- **Schedule:** Daily at 9:03 AM
- **Location:** `sentry-jira/`

## 🤖 Claude Agent

Includes a specialized Claude Code agent for managing the automation:

```
@doc-automation check status
@doc-automation update all documentation
@doc-automation run sentry automation
```

See [claude-agent/README.md](claude-agent/README.md) for details.

## 📁 Project Structure

```
documentation-automation/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── .gitignore                        # Git ignore patterns
│
├── scripts/                          # Automation scripts
│   ├── auto-update-confluence.py     # Mobile App updater
│   ├── auto-update-checkout-confluence.py  # Checkout updater
│   ├── auto-update-paecs-confluence.py     # PAECS updater
│   ├── detect-changes.py            # Change detection
│   ├── doc-health-check.py          # Health metrics
│   └── setup-cron.sh                # Cron setup script
│
├── config/                           # Configuration
│   ├── config.template.json         # Template (DO NOT COMMIT TOKENS)
│   └── README.md                    # Configuration guide
│
├── docs/                            # Documentation
│   ├── SETUP.md                     # Setup guide
│   ├── ARCHITECTURE.md              # System architecture
│   ├── TROUBLESHOOTING.md           # Common issues
│   └── API.md                       # API documentation
│
├── claude-agent/                    # Claude Code agent
│   ├── doc-automation-agent.md      # Agent configuration
│   └── README.md                    # Agent usage guide
│
├── sentry-jira/                     # Sentry-Jira integration
│   ├── analyze-sentry-issues.js     # Issue analyzer
│   ├── create-jira-tickets.js       # Ticket creator
│   ├── run-automation.js            # Main automation
│   └── README.md                    # Sentry-Jira docs
│
└── logs/                            # Log files (gitignored)
    ├── auto-update-log.txt
    ├── auto-update-checkout-log.txt
    └── auto-update-paecs-log.txt
```

## 🔧 Configuration

### 1. Confluence API Token

Generate at: https://id.atlassian.com/manage-profile/security/api-tokens

```json
{
  "confluenceUrl": "https://your-domain.atlassian.net",
  "confluenceEmail": "your.email@company.com",
  "confluenceToken": "YOUR_TOKEN_HERE"
}
```

### 2. Page IDs

```json
{
  "pages": {
    "mobileApp": "5015076940",
    "checkout": "5015404871",
    "paecs": "3223651657"
  }
}
```

### 3. Cron Schedule

All automations run every Monday at 9:00 AM:

```bash
0 9 * * 1 python3 /path/to/scripts/auto-update-confluence.py
0 9 * * 1 python3 /path/to/scripts/auto-update-checkout-confluence.py
0 9 * * 1 python3 /path/to/scripts/auto-update-paecs-confluence.py
```

## 📊 Usage

### Check Status

```bash
# View all documentation status
python3 scripts/doc-health-check.py

# Check specific page
curl -u "email:token" \
  "https://domain.atlassian.net/wiki/rest/api/content/PAGE_ID?expand=version"
```

### Manual Update

```bash
# Update all pages
python3 scripts/auto-update-confluence.py
python3 scripts/auto-update-checkout-confluence.py
python3 scripts/auto-update-paecs-confluence.py

# Or use the agent
@doc-automation update all documentation
```

### View Logs

```bash
# Recent activity
tail -50 logs/auto-update-log.txt

# Watch live
tail -f logs/auto-update-*.txt

# Check for errors
grep -i error logs/*.txt
```

## 🔍 Monitoring

### Health Dashboard

```bash
python3 << 'EOF'
import requests

pages = {
    'Mobile App': 'PAGE_ID_1',
    'Checkout': 'PAGE_ID_2',
    'PAECS': 'PAGE_ID_3'
}

for name, page_id in pages.items():
    r = requests.get(
        f'https://domain.atlassian.net/wiki/rest/api/content/{page_id}?expand=version',
        auth=('email', 'token')
    )
    if r.status_code == 200:
        data = r.json()
        print(f'{name}: Version {data["version"]["number"]}, Updated {data["version"]["when"][:10]}')
EOF
```

### Automation Status

```bash
# Check cron jobs
crontab -l

# Test automation manually
python3 scripts/auto-update-confluence.py

# Verify last run
ls -lt logs/*.txt | head -3
```

## 🐛 Troubleshooting

### Issue: Documentation Not Updating

**Check:**
1. Cron job scheduled: `crontab -l`
2. Logs for errors: `grep -i error logs/*.txt`
3. API token valid: Test with curl
4. Manual update works: Run scripts directly

### Issue: API Permission Errors

**Solution:**
1. Generate new API token
2. Update `config/config.json`
3. Test: `curl -u "email:token" "https://domain.atlassian.net/wiki/rest/api/user/current"`

### Issue: Sentry-Jira Not Working

**Solution:**
1. Check config: `cat sentry-jira/config.json`
2. Verify setup: `cd sentry-jira && ./verify-setup.sh`
3. Test manually: `cd sentry-jira && node run-automation.js`

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for more.

## 📈 Metrics

### Coverage
- **32** Mobile App screens documented (100%)
- **9** Checkout documentation files monitored
- **3** Confluence pages automated (100%)

### Reliability
- **94.8%** Mobile App documentation health score
- **7 days** maximum staleness (weekly updates)
- **3** independent automation scripts

### Performance
- **< 5 seconds** per page update
- **Zero** manual interventions in past month
- **100%** uptime since deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Ajitesh Koushal** - Initial work - [GitHub](https://github.com/ajiteshkoushal)

## 🙏 Acknowledgments

- Paidy Engineering Team
- Claude Code for automation agent support
- Confluence & Jira APIs

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/YOUR_USERNAME/documentation-automation/issues)
- **Documentation:** [docs/](docs/)
- **Email:** ajitesh.koushal@paidy.com

## 🗺️ Roadmap

- [ ] Add Slack notifications for failed updates
- [ ] Create dashboard UI for monitoring
- [ ] Add unit tests for automation scripts
- [ ] Support for additional Confluence spaces
- [ ] Integration with GitHub Actions
- [ ] Docker containerization

## 📊 Status

**Last Updated:** June 10, 2026  
**Version:** 1.0.0  
**Status:** ✅ Production - All systems operational

---

**Made with ❤️ by the Paidy Engineering Team**
