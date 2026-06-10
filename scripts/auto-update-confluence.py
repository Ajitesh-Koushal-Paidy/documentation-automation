#!/usr/bin/env python3
"""
Fully automated Confluence documentation updater
Detects changes, extracts info, and publishes automatically

Run: python3 auto-update-confluence.py
Or: Set up as cron job / GitHub Action
"""

import os
import subprocess
import json
import re
import requests
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Import configuration loader
try:
    from config_loader import get_config
    config = get_config()
except ImportError:
    # Fallback if config_loader not available
    class SimpleConfig:
        def __init__(self):
            self.base_dir = os.getenv('BASE_DIR', os.path.expanduser('~'))
            self.repo_path = os.getenv('REPO_PATH', f"{self.base_dir}/repo")
            self.confluence_url = os.getenv('CONFLUENCE_URL', 'https://your-domain.atlassian.net')
            self.confluence_email = os.getenv('CONFLUENCE_EMAIL', 'your@email.com')
            self.confluence_token = os.getenv('CONFLUENCE_API_TOKEN', '')
            self.figma_token = os.getenv('FIGMA_TOKEN', '')
        def get_page_id(self, name):
            return os.getenv(f'{name.upper()}_PAGE_ID', '')
    config = SimpleConfig()

# ============================================================================
# CONFIGURATION - LOADED FROM CONFIG FILE OR ENVIRONMENT
# ============================================================================

# Paths
REPO_PATH = config.repo_path
BASE_DIR = config.base_dir
SCREENSHOTS_DIR = config.screenshots_dir if hasattr(config, 'screenshots_dir') else f"{BASE_DIR}/figma-screenshots-individual"
API_MAPPING_FILE = f"{BASE_DIR}/screen-api-mapping.json"
MIXPANEL_MAPPING_FILE = f"{BASE_DIR}/screen-mixpanel-mapping.json"
LAST_UPDATE_FILE = f"{BASE_DIR}/.doc-last-update"
LOG_FILE = f"{BASE_DIR}/auto-update-log.txt"

# Repository directories
SCREENS_DIR = "src/screens"
QUERIES_DIR = "apollo/queries"
MIXPANEL_DIR = "vendor/Mixpanel"

# Confluence
CONFLUENCE_URL = config.confluence_url
EMAIL = config.confluence_email
CONFLUENCE_API_TOKEN = config.confluence_token
PAGE_ID = config.get_page_id('mobileApp') if hasattr(config, 'get_page_id') else os.getenv('MOBILE_APP_PAGE_ID', '')

# Figma
FIGMA_TOKEN = config.figma_token
FIGMA_FILE_KEYS = []  # Load from config if available

# Settings
DRY_RUN = False  # Set to True to test without actually updating Confluence
MIN_CHANGES_TO_UPDATE = 1  # Minimum changes before triggering update

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
# GIT OPERATIONS
# ============================================================================

def get_last_update_date():
    """Get last update date"""
    try:
        with open(LAST_UPDATE_FILE, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

def get_changed_files(since_date):
    """Get files changed since date"""
    # SECURITY FIX: Use list-based subprocess instead of shell=True
    try:
        result = subprocess.run(
            ['git', 'log', f'--since={since_date}', '--name-only', '--pretty=format:'],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            check=False
        )
        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        # Sort unique
        return sorted(set(files))
    except Exception as e:
        log(f"Error getting changed files: {e}", "ERROR")
        return []

def get_new_screens(since_date):
    """Get newly added screens"""
    # SECURITY FIX: Use list-based subprocess instead of shell=True
    try:
        result = subprocess.run(
            ['git', 'log', f'--since={since_date}', '--diff-filter=A', '--name-only', '--pretty=format:'],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            check=False
        )
        files = [f.strip() for f in result.stdout.split('\n') if f.strip() and 'Screen.tsx' in f]
        return sorted(set(files))
    except Exception as e:
        log(f"Error getting new screens: {e}", "ERROR")
        return []

def get_modified_screens(since_date):
    """Get modified screens"""
    # SECURITY FIX: Use list-based subprocess instead of shell=True
    try:
        result = subprocess.run(
            ['git', 'log', f'--since={since_date}', '--diff-filter=M', '--name-only', '--pretty=format:'],
            cwd=REPO_PATH,
            capture_output=True,
            text=True,
            check=False
        )
        files = [f.strip() for f in result.stdout.split('\n') if f.strip() and 'Screen.tsx' in f]
        return sorted(set(files))
    except Exception as e:
        log(f"Error getting modified screens: {e}", "ERROR")
        return []

# ============================================================================
# CODE ANALYSIS
# ============================================================================

def extract_apis_from_file(file_path):
    """Extract GraphQL queries, mutations, and hooks from file"""
    try:
        full_path = f"{REPO_PATH}/{file_path}"
        with open(full_path, 'r') as f:
            content = f.read()

        apis = {
            'queries': [],
            'mutations': [],
            'hooks': [],
            'imports': []
        }

        # Find GraphQL query imports
        query_pattern = r"from ['\"].*/([\w-]+\.gql)['\"]"
        apis['queries'] = re.findall(query_pattern, content)

        # Find mutation imports
        mutation_pattern = r"import.*Mutation.*from ['\"].*/([\w-]+\.gql)['\"]"
        apis['mutations'] = re.findall(mutation_pattern, content)

        # Find hooks (useQuery, useMutation, custom hooks)
        hook_pattern = r"(use[\w]+(?:Query|Mutation|Lazy|Subscription|Hook))\("
        apis['hooks'] = list(set(re.findall(hook_pattern, content)))

        return apis
    except Exception as e:
        log(f"Error extracting APIs from {file_path}: {e}", "ERROR")
        return {'queries': [], 'mutations': [], 'hooks': [], 'imports': []}

def extract_mixpanel_from_file(file_path):
    """Extract Mixpanel events from file"""
    try:
        full_path = f"{REPO_PATH}/{file_path}"
        with open(full_path, 'r') as f:
            content = f.read()

        events = {
            'page_view': None,
            'clicks': [],
            'field_edits': [],
            'success': [],
            'error': []
        }

        # Find trackPageView
        page_view_pattern = r"trackPageView\(['\"]([^'\"]+)['\"]\)"
        match = re.search(page_view_pattern, content)
        if match:
            events['page_view'] = match.group(1)

        # Find track() calls
        track_pattern = r"track\(['\"]([^'\"]+)['\"]\)"
        all_events = re.findall(track_pattern, content)

        for event in all_events:
            if 'click' in event.lower() or 'tap' in event.lower():
                events['clicks'].append(event)
            elif 'edit' in event.lower() or 'change' in event.lower():
                events['field_edits'].append(event)
            elif 'success' in event.lower() or 'complete' in event.lower():
                events['success'].append(event)
            elif 'error' in event.lower() or 'fail' in event.lower():
                events['error'].append(event)

        return events
    except Exception as e:
        log(f"Error extracting Mixpanel from {file_path}: {e}", "ERROR")
        return {'page_view': None, 'clicks': [], 'field_edits': [], 'success': [], 'error': []}

def generate_screen_description(file_path, screen_name):
    """Generate screen description from code analysis"""
    try:
        full_path = f"{REPO_PATH}/{file_path}"
        with open(full_path, 'r') as f:
            content = f.read()

        # Extract JSDoc comments or top-level comments
        comment_pattern = r'/\*\*\n(.*?)\*/'
        comments = re.findall(comment_pattern, content, re.DOTALL)

        if comments:
            return comments[0].strip().replace('*', '').strip()

        # Fallback: Generic description based on screen name
        name_clean = screen_name.replace('Screen', '').replace('-', ' ').title()
        return f"Screen for {name_clean} functionality. Auto-generated description - please review and enhance."

    except Exception as e:
        log(f"Error generating description for {file_path}: {e}", "ERROR")
        return f"Screen documentation - please add description"

# ============================================================================
# FIGMA OPERATIONS
# ============================================================================

def find_figma_node_id(screen_name):
    """Try to find Figma node ID for screen (search across files)"""
    # This is a simplified version - you might need to map screens to Figma nodes manually
    # or maintain a mapping file

    # For now, return None (manual extraction needed)
    # In a production system, you'd search Figma API for matching frame names
    return None

def extract_figma_screenshot(node_id, file_key):
    """Extract screenshot from Figma"""
    if not node_id:
        return None

    try:
        url = f"https://api.figma.com/v1/images/{file_key}"
        params = {"ids": node_id, "scale": 3, "format": "png"}
        headers = {"X-Figma-Token": FIGMA_TOKEN}

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            image_url = data.get('images', {}).get(node_id)

            if image_url:
                # Download image
                img_response = requests.get(image_url)
                return img_response.content

        return None
    except Exception as e:
        log(f"Error extracting Figma screenshot: {e}", "ERROR")
        return None

# ============================================================================
# DATA MANAGEMENT
# ============================================================================

def load_mappings():
    """Load existing mappings"""
    try:
        with open(API_MAPPING_FILE, 'r') as f:
            api_mappings = json.load(f)
    except FileNotFoundError:
        api_mappings = {}

    try:
        with open(MIXPANEL_MAPPING_FILE, 'r') as f:
            mixpanel_mappings = json.load(f)
    except FileNotFoundError:
        mixpanel_mappings = {}

    return api_mappings, mixpanel_mappings

def save_mappings(api_mappings, mixpanel_mappings):
    """Save updated mappings"""
    with open(API_MAPPING_FILE, 'w') as f:
        json.dump(api_mappings, f, indent=2)

    with open(MIXPANEL_MAPPING_FILE, 'w') as f:
        json.dump(mixpanel_mappings, f, indent=2)

def update_mappings_for_screen(screen_file, api_mappings, mixpanel_mappings):
    """Update mappings for a specific screen"""
    screen_name = Path(screen_file).stem
    screen_id = screen_name.lower().replace('screen', '-screen')

    # Extract APIs
    apis = extract_apis_from_file(screen_file)

    # Extract Mixpanel
    mixpanel = extract_mixpanel_from_file(screen_file)

    # Generate description
    description = generate_screen_description(screen_file, screen_name)

    # Update API mapping
    if screen_id not in api_mappings:
        api_mappings[screen_id] = {}

    api_mappings[screen_id].update({
        'screen_name': screen_name,
        'file_path': screen_file,
        'graphql_queries': apis['queries'],
        'graphql_mutations': apis['mutations'],
        'hooks': apis['hooks'],
        'description': description,
        'last_updated': datetime.now().strftime('%Y-%m-%d')
    })

    # Update Mixpanel mapping
    if mixpanel['page_view'] or mixpanel['clicks']:
        mixpanel_mappings[screen_id] = {
            'screen_name': screen_name,
            'page_view': mixpanel['page_view'],
            'clicks': mixpanel['clicks'],
            'field_edits': mixpanel['field_edits'],
            'success': mixpanel['success'],
            'error': mixpanel['error'],
            'last_updated': datetime.now().strftime('%Y-%m-%d')
        }

    return api_mappings, mixpanel_mappings

# ============================================================================
# CONFLUENCE OPERATIONS
# ============================================================================

def update_confluence_page():
    """Update Confluence page with latest data"""
    log("Updating Confluence page...")

    try:
        # This would call your existing update-confluence-final.py logic
        # For simplicity, we'll use subprocess
        result = subprocess.run(
            ['python3', f'{BASE_DIR}/update-confluence-final.py'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            log("✅ Confluence page updated successfully")
            return True
        else:
            log(f"❌ Confluence update failed: {result.stderr}", "ERROR")
            return False

    except Exception as e:
        log(f"❌ Error updating Confluence: {e}", "ERROR")
        return False

def update_last_modified_date():
    """Update the 'Last Updated' date in Confluence"""
    try:
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
        today = datetime.now().strftime('%B %d, %Y')
        content = re.sub(
            r'Last Updated:</strong> [^<]+',
            f'Last Updated:</strong> {today}',
            content
        )

        # Add auto-update notice if not present
        if '🤖 Auto-updated' not in content:
            notice = '<p><em>🤖 Auto-updated via automation script</em></p>'
            # Insert before closing tags
            content = content.replace('</ac:structured-macro>\n<p><em>🤖 Generated',
                                     f'</ac:structured-macro>\n{notice}\n<p><em>🤖 Generated')

        # Update page
        payload = {
            'id': PAGE_ID,
            'type': 'page',
            'title': 'Paidy Mobile App - Complete Documentation',
            'body': {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            },
            'version': {'number': version + 1}
        }

        response = requests.put(url, auth=auth, headers=headers, data=json.dumps(payload))

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
    log("🤖 AUTOMATED CONFLUENCE DOCUMENTATION UPDATE")
    log("=" * 80)

    # Check configuration
    if REPO_PATH == "/path/to/paidy-app-rn":
        log("❌ REPO_PATH not configured. Please update auto-update-confluence.py", "ERROR")
        return

    # Get last update date
    last_update = get_last_update_date()
    log(f"Last update: {last_update}")

    # Detect changes
    log("Detecting changes...")
    changed_files = get_changed_files(last_update)
    new_screens = get_new_screens(last_update)
    modified_screens = get_modified_screens(last_update)

    log(f"Found {len(changed_files)} changed files")
    log(f"  - {len(new_screens)} new screens")
    log(f"  - {len(modified_screens)} modified screens")

    # Check if update needed
    total_changes = len(new_screens) + len(modified_screens)

    if total_changes < MIN_CHANGES_TO_UPDATE:
        log("✅ No significant changes detected. Documentation is up to date.")

        # Still update the date to show it's being monitored
        if not DRY_RUN:
            update_last_modified_date()

        # Update last check time
        with open(LAST_UPDATE_FILE, 'w') as f:
            f.write(datetime.now().strftime('%Y-%m-%d'))

        return

    log(f"⚠️  {total_changes} screens need updates")

    # Load mappings
    log("Loading existing mappings...")
    api_mappings, mixpanel_mappings = load_mappings()

    # Process new screens
    updated_count = 0
    for screen_file in new_screens:
        log(f"Processing NEW screen: {screen_file}")
        api_mappings, mixpanel_mappings = update_mappings_for_screen(
            screen_file, api_mappings, mixpanel_mappings
        )
        updated_count += 1

    # Process modified screens
    for screen_file in modified_screens:
        log(f"Processing MODIFIED screen: {screen_file}")
        api_mappings, mixpanel_mappings = update_mappings_for_screen(
            screen_file, api_mappings, mixpanel_mappings
        )
        updated_count += 1

    # Save mappings
    if not DRY_RUN:
        log("Saving updated mappings...")
        save_mappings(api_mappings, mixpanel_mappings)
        log(f"✅ Updated {updated_count} screen mappings")
    else:
        log(f"[DRY RUN] Would update {updated_count} screen mappings")

    # Update Confluence
    if not DRY_RUN:
        log("Publishing to Confluence...")
        success = update_confluence_page()

        if success:
            # Update last modified date
            update_last_modified_date()

            # Update last check time
            with open(LAST_UPDATE_FILE, 'w') as f:
                f.write(datetime.now().strftime('%Y-%m-%d'))

            log("=" * 80)
            log("✅ AUTOMATION COMPLETE")
            log(f"   Updated {updated_count} screens")
            log(f"   Confluence: https://paidy-portal.atlassian.net/wiki/spaces/~597796370/pages/{PAGE_ID}")
            log("=" * 80)
        else:
            log("❌ Confluence update failed", "ERROR")
    else:
        log("[DRY RUN] Would update Confluence page")
        log(f"[DRY RUN] Processed {updated_count} screens")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log(f"❌ Fatal error: {e}", "ERROR")
        raise
