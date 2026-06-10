#!/usr/bin/env python3
"""
Check documentation health metrics
Run: python3 doc-health-check.py
"""

import json
from pathlib import Path
from datetime import datetime

def check_health():
    """Generate health report"""

    print("=" * 80)
    print("📊 DOCUMENTATION HEALTH CHECK")
    print("=" * 80)
    print()

    try:
        # Load mappings
        with open('/Users/ajitesh.koushal/screen-api-mapping.json') as f:
            api_mappings = json.load(f)

        with open('/Users/ajitesh.koushal/screen-mixpanel-mapping.json') as f:
            mixpanel_mappings = json.load(f)

        # Count screens
        total_screens = len(api_mappings)
        screens_with_apis = sum(1 for s in api_mappings.values()
                               if s.get('graphql_queries') or s.get('graphql_mutations') or s.get('hooks'))
        screens_with_mixpanel = len(mixpanel_mappings)

        # Screenshots
        screenshots_dir = Path('/Users/ajitesh.koushal/figma-screenshots-individual')
        screenshots_count = 0
        if screenshots_dir.exists():
            screenshots_count = len(list(screenshots_dir.glob('*.png')))

        # Coverage percentages
        api_coverage = (screens_with_apis / total_screens * 100) if total_screens > 0 else 0
        mixpanel_coverage = (screens_with_mixpanel / total_screens * 100) if total_screens > 0 else 0
        screenshot_coverage = (screenshots_count / total_screens * 100) if total_screens > 0 else 0

        # Overall health score
        health_score = (api_coverage + mixpanel_coverage + screenshot_coverage) / 3

        # Generate report
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print()
        print("📈 Coverage Metrics")
        print("-" * 80)
        print(f"  Screens Documented:     {total_screens}")
        print(f"  API Mappings:           {screens_with_apis}/{total_screens} ({api_coverage:.1f}%)")
        print(f"  Mixpanel Events:        {screens_with_mixpanel}/{total_screens} ({mixpanel_coverage:.1f}%)")
        print(f"  Screenshots:            {screenshots_count}/{total_screens} ({screenshot_coverage:.1f}%)")
        print()
        print("🎯 Health Score")
        print("-" * 80)

        # Health score with color
        if health_score >= 90:
            status = "✅ EXCELLENT"
        elif health_score >= 75:
            status = "✅ GOOD"
        elif health_score >= 60:
            status = "⚠️  NEEDS IMPROVEMENT"
        else:
            status = "❌ CRITICAL"

        print(f"  Overall:                {health_score:.1f}% {status}")
        print()

        # Missing coverage
        screens_missing_apis = total_screens - screens_with_apis
        screens_missing_mixpanel = total_screens - screens_with_mixpanel
        screens_missing_screenshots = total_screens - screenshots_count

        if screens_missing_apis > 0 or screens_missing_mixpanel > 0 or screens_missing_screenshots > 0:
            print("⚠️  Missing Coverage")
            print("-" * 80)
            if screens_missing_apis > 0:
                print(f"  {screens_missing_apis} screens missing API mappings")
            if screens_missing_mixpanel > 0:
                print(f"  {screens_missing_mixpanel} screens missing Mixpanel events")
            if screens_missing_screenshots > 0:
                print(f"  {screens_missing_screenshots} screens missing screenshots")
            print()

        # Recommendations
        print("💡 Recommendations")
        print("-" * 80)
        if health_score >= 90:
            print("  • Excellent! Run weekly checks to maintain quality")
            print("  • Consider adding more detailed descriptions")
        elif health_score >= 75:
            print("  • Good coverage, focus on filling gaps")
            print("  • Add missing screenshots from Figma")
        elif health_score >= 60:
            print("  • Priority: Complete API and Mixpanel mappings")
            print("  • Extract missing screenshots from Figma")
        else:
            print("  • URGENT: Significant gaps in documentation")
            print("  • Run update scripts to improve coverage")
        print()

        # Quick actions
        print("🔧 Quick Actions")
        print("-" * 80)
        print("  1. Check for changes:       python3 detect-changes.py")
        print("  2. Update API mappings:     Edit screen-api-mapping.json")
        print("  3. Update Mixpanel events:  Edit screen-mixpanel-mapping.json")
        print("  4. Update Confluence:       python3 update-confluence-final.py")
        print()

        print("🔗 Resources")
        print("-" * 80)
        print("  Confluence: https://paidy-portal.atlassian.net/wiki/spaces/~597796370/pages/5015076940")
        print("  GitHub:     https://github.com/paidy/paidy-app-rn")
        print()

        print("=" * 80)
        print(f"Next recommended check: {(datetime.now()).strftime('%Y-%m-%d')}")
        print("=" * 80)

    except FileNotFoundError as e:
        print(f"❌ Error: Missing file - {e}")
        print("   Make sure API and Mixpanel mapping files exist")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_health()
