#!/bin/bash
# Helper script to push repository to GitHub

echo "🚀 GitHub Push Helper"
echo "===================="
echo ""
echo "First, create your repository on GitHub:"
echo "  👉 https://github.com/new"
echo ""
echo "Settings:"
echo "  - Name: documentation-automation"
echo "  - Visibility: Public"
echo "  - DO NOT initialize with README, .gitignore, or license"
echo ""
echo "After creating the repository, GitHub will show you a URL like:"
echo "  https://github.com/YOUR_USERNAME/documentation-automation.git"
echo ""
read -p "Enter your GitHub repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No URL provided. Exiting."
    exit 1
fi

echo ""
echo "📝 Repository URL: $REPO_URL"
echo ""
read -p "Is this correct? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled. Please run again with correct URL."
    exit 1
fi

echo ""
echo "🔗 Adding remote..."
git remote add origin "$REPO_URL"

if [ $? -ne 0 ]; then
    echo "⚠️  Remote already exists. Updating..."
    git remote set-url origin "$REPO_URL"
fi

echo ""
echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Repository published to GitHub!"
    echo ""
    echo "📊 View your repository:"
    echo "  ${REPO_URL%.git}"
    echo ""
    echo "🎯 Next steps:"
    echo "  1. Add topics: confluence, automation, documentation, python"
    echo "  2. Edit description if needed"
    echo "  3. Share with your team!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Common issues:"
    echo "  - Check you're logged in to GitHub"
    echo "  - Verify repository was created"
    echo "  - Try: git remote -v"
    echo ""
fi
