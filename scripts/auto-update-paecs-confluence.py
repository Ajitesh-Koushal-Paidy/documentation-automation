#!/usr/bin/env python3
import os
"""
Automated Confluence documentation updater for PAECS Handbook
Updates the "Last Updated" date automatically

Run: python3 auto-update-paecs-confluence.py
Or: Set up as cron job
"""

import requests
import json
import re
from datetime import datetime, timedelta

# ============================================================================
# CONFIGURATION
# ============================================================================

# Local paths
BASE_DIR = "/Users/ajitesh.koushal"
LAST_UPDATE_FILE = f"{BASE_DIR}/.paecs-doc-last-update"
LOG_FILE = f"{BASE_DIR}/auto-update-paecs-log.txt"

# Confluence
CONFLUENCE_URL = "https://paidy-portal.atlassian.net"
EMAIL = "ajitesh.koushal@paidy.com"
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN", "YOUR_TOKEN_HERE")
PAGE_ID = "3223651657"

# Settings
DRY_RUN = False  # Set to True to test without updating

# ============================================================================
# LOGGING
# ============================================================================

def log(message, level="INFO"):
    """Write to log file and console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] [{level}] {message}"
    print(log_message)

    with open(LOG_FILE, 'a') as f:
        f.write(log_message + '\n')

# ============================================================================
# CONFLUENCE OPERATIONS
# ============================================================================

def get_last_update_date():
    """Get last update date"""
    try:
        with open(LAST_UPDATE_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def save_last_update_date():
    """Save current date as last update"""
    with open(LAST_UPDATE_FILE, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d'))

def update_paecs_page():
    """Update PAECS Handbook page with current date"""
    try:
        auth = (EMAIL, CONFLUENCE_API_TOKEN)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Get current page
        url = f"{CONFLUENCE_URL}/wiki/rest/api/content/{PAGE_ID}?expand=version,body.storage"
        response = requests.get(url, auth=auth, headers=headers)

        if response.status_code != 200:
            log(f"Failed to fetch page: {response.status_code}", "ERROR")
            return False

        data = response.json()
        content = data['body']['storage']['value']
        version = data['version']['number']
        title = data['title']

        # Update date
        today = datetime.now().strftime('%B %d, %Y')

        # Check if date field exists
        if 'Last updated' in content or 'Last Updated' in content:
            log("Updating existing date...")
            content = re.sub(
                r'<p><em>Last [Uu]pdated:.*?</em></p>',
                f'<p><em>Last Updated: {today} | Maintained by: Customer Support Team</em></p>',
                content
            )
        else:
            log("Adding new date field...")
            date_block = f'<hr/><p><em>Last Updated: {today} | Maintained by: Customer Support Team</em></p>'
            content = content.rstrip() + '\n' + date_block

        # Update page
        payload = {
            'id': PAGE_ID,
            'type': 'page',
            'title': title,
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            },
            'version': {'number': version + 1}
        }

        response = requests.put(url, auth=auth, headers=headers, json=payload)

        if response.status_code == 200:
            log(f"✅ Updated '{title}' to version {version + 1}")
            log(f"✅ Date updated to {today}")
            return True
        else:
            log(f"❌ Failed to update: {response.status_code}", "ERROR")
            return False

    except Exception as e:
        log(f"❌ Error: {e}", "ERROR")
        return False

# ============================================================================
# MAIN AUTOMATION
# ============================================================================

def main():
    """Main automation flow"""

    log("=" * 80)
    log("🤖 AUTOMATED PAECS HANDBOOK UPDATE")
    log("=" * 80)

    last_update = get_last_update_date()
    today = datetime.now().strftime('%Y-%m-%d')

    if last_update:
        log(f"Last update: {last_update}")

        # Check if we need to update (once per week)
        last_date = datetime.strptime(last_update, '%Y-%m-%d')
        days_since = (datetime.now() - last_date).days

        if days_since < 7:
            log(f"✅ Updated {days_since} days ago. Next update in {7 - days_since} days.")
            return
    else:
        log("First run - will update page")

    # Update page
    if not DRY_RUN:
        log("Updating PAECS Handbook...")
        success = update_paecs_page()

        if success:
            save_last_update_date()
            log("=" * 80)
            log("✅ AUTOMATION COMPLETE")
            log(f"   URL: {CONFLUENCE_URL}/wiki/spaces/UXE/pages/{PAGE_ID}")
            log("=" * 80)
        else:
            log("❌ Update failed", "ERROR")
    else:
        log("[DRY RUN] Would update PAECS page")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"❌ Fatal error: {e}", "ERROR")
        raise
