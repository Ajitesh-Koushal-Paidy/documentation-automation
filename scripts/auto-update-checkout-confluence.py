#!/usr/bin/env python3
"""
Automated Confluence documentation updater for Checkout
Monitors markdown files and updates Confluence when changes detected

Run: python3 auto-update-checkout-confluence.py
Or: Set up as cron job
"""

import subprocess
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# Import configuration loader
try:
    from config_loader import get_config
    config = get_config()
except ImportError:
    class SimpleConfig:
        def __init__(self):
            self.base_dir = os.getenv('BASE_DIR', os.path.expanduser('~'))
            self.confluence_url = os.getenv('CONFLUENCE_URL', 'https://your-domain.atlassian.net')
            self.confluence_email = os.getenv('CONFLUENCE_EMAIL', 'your@email.com')
            self.confluence_token = os.getenv('CONFLUENCE_API_TOKEN', '')
        def get_page_id(self, name):
            return os.getenv(f'{name.upper()}_PAGE_ID', '')
    config = SimpleConfig()

# ============================================================================
# CONFIGURATION - LOADED FROM CONFIG FILE OR ENVIRONMENT
# ============================================================================

# Paths
BASE_DIR = config.base_dir
LAST_UPDATE_FILE = f"{BASE_DIR}/.checkout-doc-last-update"
LOG_FILE = f"{BASE_DIR}/auto-update-checkout-log.txt"

# Documentation files to monitor
DOC_FILES = [
    f"{BASE_DIR}/checkout-flows-complete.md",
    f"{BASE_DIR}/checkout-flows-additional.md",
    f"{BASE_DIR}/checkout-flows-additional-part2.md",
    f"{BASE_DIR}/checkout-technical-docs.md",
    f"{BASE_DIR}/checkout-technical-docs-part2.md",
    f"{BASE_DIR}/checkout-docs-newcomer-friendly.md",
    f"{BASE_DIR}/checkout-additional-sections.md",
    f"{BASE_DIR}/checkout-uxe-additions.md",
    f"{BASE_DIR}/checkout-merchant-integration-docs.md",
]

# Confluence
CONFLUENCE_URL = config.confluence_url
EMAIL = config.confluence_email
CONFLUENCE_API_TOKEN = config.confluence_token
PAGE_ID = config.get_page_id('checkout') if hasattr(config, 'get_page_id') else os.getenv('CHECKOUT_PAGE_ID', '')

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
# FILE MONITORING
# ============================================================================

def get_file_hash(file_path):
    """Get MD5 hash of file content"""
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except FileNotFoundError:
        return None

def get_last_hashes():
    """Get stored file hashes from last update"""
    try:
        with open(LAST_UPDATE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_current_hashes(hashes):
    """Save current file hashes"""
    with open(LAST_UPDATE_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)

def detect_changes():
    """Check if any documentation files have changed"""
    last_hashes = get_last_hashes()
    current_hashes = {}
    changed_files = []

    for file_path in DOC_FILES:
        if os.path.exists(file_path):
            current_hash = get_file_hash(file_path)
            current_hashes[file_path] = current_hash

            # Check if changed
            if file_path not in last_hashes or last_hashes[file_path] != current_hash:
                changed_files.append(file_path)

    return changed_files, current_hashes

# ============================================================================
# CONFLUENCE OPERATIONS
# ============================================================================

def update_confluence_page():
    """Update Confluence page using the main update script"""
    log("Updating Confluence page...")

    try:
        result = subprocess.run(
            ['python3', f'{BASE_DIR}/update_confluence_with_merchant_docs.py'],
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            log("✅ Confluence page updated successfully")
            return True
        else:
            log(f"❌ Confluence update failed: {result.stderr}", "ERROR")
            return False

    except subprocess.TimeoutExpired:
        log("❌ Confluence update timed out", "ERROR")
        return False
    except Exception as e:
        log(f"❌ Error updating Confluence: {e}", "ERROR")
        return False

def update_last_modified_date():
    """Update only the 'Last Updated' date in Confluence"""
    try:
        import requests

        auth = (EMAIL, CONFLUENCE_API_TOKEN)
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Get current page
        url = f"{CONFLUENCE_URL}/wiki/rest/api/content/{PAGE_ID}?expand=body.storage,version"
        response = requests.get(url, auth=auth, headers=headers)

        if response.status_code != 200:
            log(f"Failed to fetch Confluence page: {response.status_code}", "ERROR")
            return False

        data = response.json()
        content = data['body']['storage']['value']
        version = data['version']['number']

        # Update date
        today = datetime.now().strftime('%Y-%m-%d')
        import re
        content = re.sub(
            r'Last updated: \d{4}-\d{2}-\d{2}',
            f'Last updated: {today}',
            content
        )

        # Update page
        payload = {
            'id': PAGE_ID,
            'type': 'page',
            'title': 'Paidy Checkout - Complete Documentation (Internal + Merchant Integration)',
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
            log(f"✅ Updated 'Last Updated' date to {today}")
            return True
        else:
            log(f"❌ Failed to update date: {response.status_code}", "ERROR")
            return False

    except Exception as e:
        log(f"❌ Error updating date: {e}", "ERROR")
        return False

# ============================================================================
# MAIN AUTOMATION
# ============================================================================

def main():
    """Main automation flow"""

    log("=" * 80)
    log("🤖 AUTOMATED CHECKOUT DOCUMENTATION UPDATE")
    log("=" * 80)

    # Detect changes
    log("Checking for documentation changes...")
    changed_files, current_hashes = detect_changes()

    log(f"Monitoring {len(DOC_FILES)} documentation files")
    log(f"Found {len(changed_files)} changed files")

    if changed_files:
        log("Changed files:")
        for file_path in changed_files:
            log(f"  - {Path(file_path).name}")

    # Check if update needed
    if len(changed_files) == 0:
        log("✅ No changes detected. Documentation is up to date.")

        # Still update the date to show monitoring is active
        if not DRY_RUN:
            update_last_modified_date()

        return

    log(f"⚠️  {len(changed_files)} files changed - updating documentation")

    # Update Confluence
    if not DRY_RUN:
        log("Publishing to Confluence...")
        success = update_confluence_page()

        if success:
            # Save current hashes
            save_current_hashes(current_hashes)

            log("=" * 80)
            log("✅ AUTOMATION COMPLETE")
            log(f"   Updated {len(changed_files)} files")
            log(f"   Confluence: {CONFLUENCE_URL}/wiki/spaces/UXE/pages/{PAGE_ID}")
            log("=" * 80)
        else:
            log("❌ Confluence update failed", "ERROR")
    else:
        log("[DRY RUN] Would update Confluence page")
        log(f"[DRY RUN] Processed {len(changed_files)} changed files")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"❌ Fatal error: {e}", "ERROR")
        raise
