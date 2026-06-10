# Documentation Automation Agent - User Guide

**Created:** June 10, 2026  
**Status:** ✅ Active & Ready

---

## 🤖 What Is This Agent?

The **Documentation Automation Agent** is a specialized Claude agent that manages:

1. **Three Confluence Documentation Pages**
   - Mobile App Documentation
   - Checkout Documentation  
   - PAECS Handbook

2. **Sentry-Jira Automation**
   - Monitors Sentry errors
   - Creates Jira tickets for quick fixes

---

## 🚀 How to Use the Agent

### Invoke the Agent

In Claude Code, type:
```
@doc-automation [your request]
```

Or use the full path:
```
Ask the doc-automation agent to check documentation status
```

---

## 📝 Common Commands

### Check All Documentation Status
```
@doc-automation check documentation status
```
Shows current version and last updated date for all three pages.

### Update All Documentation
```
@doc-automation update all documentation
```
Manually triggers updates for all three Confluence pages.

### Run Sentry-Jira Automation
```
@doc-automation run sentry jira automation
```
Analyzes Sentry issues and creates Jira tickets for quick fixes.

### View Documentation Logs
```
@doc-automation show me the recent logs
```
Displays recent activity from all automation scripts.

### Check Documentation Health
```
@doc-automation check mobile app health
```
Shows Mobile App documentation health score and coverage metrics.

### Setup Sentry-Jira
```
@doc-automation setup sentry automation
```
Guides you through Sentry-Jira automation configuration.

---

## 📊 What the Agent Manages

### 1. Mobile App Documentation

**Page:** [Mobile App - Complete Documentation](https://paidy-portal.atlassian.net/wiki/spaces/UXE/pages/5015076940)

**Features:**
- Monitors Git repository for changes
- Tracks 32 screens
- Updates API mappings
- Monitors Mixpanel events
- Health score: 94.8%

**Automation:**
- Script: `auto-update-confluence.py`
- Schedule: Every Monday 9 AM
- Logs: `auto-update-log.txt`

### 2. Checkout Documentation

**Page:** [Checkout - Complete Documentation](https://paidy-portal.atlassian.net/wiki/spaces/UXE/pages/5015404871)

**Features:**
- Monitors 9 markdown files
- Tracks flows, technical docs, merchant integration
- MD5 hash-based change detection

**Automation:**
- Script: `auto-update-checkout-confluence.py`
- Schedule: Every Monday 9 AM
- Logs: `auto-update-checkout-log.txt`

### 3. PAECS Handbook

**Page:** [PAECS Handbook](https://paidy-portal.atlassian.net/wiki/spaces/UXE/pages/3223651657)

**Features:**
- Weekly date refresh
- Simple maintenance update

**Automation:**
- Script: `auto-update-paecs-confluence.py`
- Schedule: Every Monday 9 AM
- Logs: `auto-update-paecs-log.txt`

### 4. Sentry-Jira Automation

**Location:** `~/.claude/scripts/sentry-jira-automation/`

**Features:**
- Analyzes Sentry errors for quick fix opportunities
- Creates Jira tickets in BDPA project
- Includes problem description, solution steps, file paths
- Estimated effort: 5-15 minutes per ticket

**Automation:**
- Schedule: Daily at 9:03 AM
- Status: Needs initial configuration

---

## 🎯 Example Interactions

### Example 1: Daily Status Check
```
You: @doc-automation what's the current status?

Agent: 📊 Documentation Status Dashboard
        
        Mobile App: ✅ Version 20, Updated 2026-06-09
        Checkout: ✅ Version 18, Updated 2026-06-09
        PAECS: ✅ Version 12, Updated 2026-06-09
        
        All systems operational. Next update: Monday 9 AM
```

### Example 2: Manual Update
```
You: @doc-automation update the checkout documentation

Agent: Updating Checkout documentation...
       ✅ Updated to version 19
       ✅ Date refreshed to June 10, 2026
       ✅ All changes published
```

### Example 3: Sentry Automation
```
You: @doc-automation run the sentry automation

Agent: Checking Sentry-Jira automation...
       ⚠️  Configuration needed. Would you like me to set it up?
       I need your Sentry auth token to proceed.
```

### Example 4: Troubleshooting
```
You: @doc-automation why didn't the mobile app update today?

Agent: Checking logs...
       ✅ Last update: June 09, 2026
       📅 Next scheduled: June 16, 2026 (Monday 9 AM)
       ℹ️  No update today because it only runs on Mondays
       
       To update manually: [commands shown]
```

---

## 🔧 Agent Capabilities

### What the Agent Can Do

✅ **Check status** of all documentation pages  
✅ **Run manual updates** for any page  
✅ **View logs** and diagnose issues  
✅ **Check documentation health** (Mobile App)  
✅ **Setup Sentry-Jira** automation  
✅ **Run Sentry-Jira** automation  
✅ **Verify API tokens** and connectivity  
✅ **Show cron schedules**  
✅ **Troubleshoot** common issues  

### What the Agent Cannot Do

❌ Create new documentation pages  
❌ Modify documentation content (only dates)  
❌ Change API tokens (but can verify them)  
❌ Access Sentry without token  
❌ Modify cron schedules (but can show them)  

---

## 📅 Automation Schedule

### Weekly Updates (Every Monday 9:00 AM)
- Mobile App Documentation
- Checkout Documentation
- PAECS Handbook

### Daily Updates (Every Day 9:03 AM)
- Sentry-Jira Automation (once configured)

---

## 🔍 Troubleshooting with the Agent

### Documentation Not Updating

```
@doc-automation troubleshoot mobile app updates
```

Agent will:
1. Check cron schedule
2. Review recent logs
3. Verify API token
4. Test manual update
5. Provide specific fix recommendations

### Sentry-Jira Not Working

```
@doc-automation troubleshoot sentry automation
```

Agent will:
1. Check if config exists
2. Verify setup
3. Test API connections
4. Show recent run results
5. Guide through reconfiguration if needed

---

## 📞 Getting Help from the Agent

### Ask Questions

```
@doc-automation when was the checkout page last updated?
@doc-automation what's the health score of mobile app docs?
@doc-automation show me the cron schedule
@doc-automation how do I force an update?
```

### Request Actions

```
@doc-automation update all pages now
@doc-automation check if the API token is valid
@doc-automation show me errors from the last week
@doc-automation setup sentry automation for me
```

---

## 🎓 Advanced Usage

### Custom Workflows

```
@doc-automation do a full system check
```
Agent will:
- Check all three documentation pages
- Verify all cron jobs
- Review all logs for errors
- Test API connectivity
- Show comprehensive status report

### Batch Operations

```
@doc-automation update all documentation and show me the health report
```
Agent can chain multiple operations together.

---

## 🔐 Security Notes

- Agent has access to API tokens (stored in agent config)
- Tokens are never displayed in full (only first/last 10 chars)
- All API calls are logged
- Agent cannot modify tokens, only use them

---

## 📋 Agent Configuration

**Location:** `/Users/ajitesh.koushal/.claude/agents/doc-automation-agent.md`

**Model:** Claude Sonnet 4.5  

**Knowledge Base:**
- All three documentation systems
- Cron schedules and automation scripts
- API endpoints and tokens
- Troubleshooting procedures
- Log file locations

---

## 🎯 Best Practices

### Daily Use

- **Morning:** `@doc-automation check status` to see overnight updates
- **After changes:** `@doc-automation update [specific page]` for immediate refresh
- **Weekly:** Let automation run on Mondays, check logs Tuesday

### Troubleshooting

- **Always start with:** `@doc-automation check status`
- **Review logs:** `@doc-automation show logs`
- **Test manually** before assuming automation is broken

### Sentry-Jira

- **Setup once:** Provide Sentry token when prompted
- **Let it run:** Daily automation handles the rest
- **Review tickets:** Check BDPA board for new quick fix opportunities

---

## 📝 Quick Reference

### Common Agent Commands

| Command | What It Does |
|---------|--------------|
| `check status` | Shows all pages status |
| `update all` | Updates all three pages |
| `update [page]` | Updates specific page |
| `show logs` | Displays recent logs |
| `health check` | Mobile App health score |
| `run sentry` | Runs Sentry-Jira automation |
| `setup sentry` | Configures Sentry automation |
| `troubleshoot [system]` | Diagnoses issues |

---

## ✅ Summary

**Agent Name:** `doc-automation`  
**Purpose:** Manage documentation updates and Sentry-Jira automation  
**Status:** ✅ Active and ready to use  
**Invoke:** `@doc-automation [your request]`

**Manages:**
- ✅ Mobile App Documentation (32 screens)
- ✅ Checkout Documentation (9 files)
- ✅ PAECS Handbook (weekly updates)
- ✅ Sentry-Jira Automation (quick fix tickets)

**Schedule:**
- 📅 Monday 9:00 AM: Documentation updates
- 📅 Daily 9:03 AM: Sentry-Jira automation

---

**The agent is ready to help you manage all documentation automation! Just invoke it with `@doc-automation` and ask your question.** 🤖
