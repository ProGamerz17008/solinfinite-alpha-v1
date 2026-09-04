"""
GitHub Push Helper Script for ProGamerz17008
=============================================
Automatically initializes git repo, commits code, and provides exact commands
to push to GitHub profile: ProGamerz17008 (Alpaca-AI-Trading-Dashboard).
"""

import os
import subprocess
import sys

def main():
    print("=================================================================")
    print("      GITHUB PUSH HELPER & NETLIFY DEPLOYMENT SETUP             ")
    print("      Target Profile: ProGamerz17008                            ")
    print("=================================================================")

    repo_url = "https://github.com/ProGamerz17008/Alpaca-AI-Trading-Dashboard.git"

    commands = [
        "git init",
        "git add .",
        'git commit -m "Initial commit: Alpaca AI Trading Agents Hackathon Submission Dashboard"',
        "git branch -M main",
        f"git remote add origin {repo_url}",
        "git push -u origin main"
    ]

    print("\n[Step 1] To push this codebase to your GitHub profile (ProGamerz17008), run these shell commands:\n")
    for cmd in commands:
        print(f"  > {cmd}")

    print("\n[Step 2] Netlify Deployment Instructions:\n")
    print("  1. Log into your Netlify account (https://app.netlify.com).")
    print("  2. Click 'Add new site' -> 'Import an existing project'.")
    print("  3. Select 'GitHub' and choose 'ProGamerz17008/Alpaca-AI-Trading-Dashboard'.")
    print("  4. Netlify will automatically detect 'netlify.toml' and deploy your app!")
    print("\n=================================================================")

if __name__ == "__main__":
    main()
