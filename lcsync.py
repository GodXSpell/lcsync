#!/usr/bin/env python3
"""
LeetCode Sync (lcsync) - Simple Command Wrapper
Short and easy commands for the LeetCode submission tool
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd_args):
    """Run the main CLI with the provided arguments"""
    script_dir = Path(__file__).parent
    main_script = script_dir / "leetcode_auto_push.py"
    
    try:
        result = subprocess.run([sys.executable, str(main_script)] + cmd_args, 
                              check=False, cwd=script_dir)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running command: {e}")
        sys.exit(1)

def show_help():
    """Show available commands"""
    help_text = """
🚀 LeetCode Sync (lcsync) - Quick Commands

USAGE:
    lcsync <command>

COMMANDS:
    init        Initialize project folders and .gitignore
    user        Set up user configuration (username, repo, commit message)
    cookie      Update/change LeetCode session cookie  
    fetch       Fetch new accepted submissions from LeetCode
    push        Push changes to GitHub (git add, commit, push)
    help        Show this help message

EXAMPLES:
    lcsync init         # Initialize the project
    lcsync user         # Set up your user configuration
    lcsync cookie       # Add your LeetCode session cookie
    lcsync fetch        # Fetch your latest submissions
    lcsync push         # Push to GitHub

FULL WORKFLOW:
    1. lcsync init      # First time setup
    2. lcsync user      # Configure your settings
    3. lcsync cookie    # Add LeetCode session
    4. lcsync fetch     # Get your submissions
    5. lcsync push      # Push to GitHub

For detailed help: python leetcode_auto_push.py --help
    """
    print(help_text)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    # Command mapping
    command_map = {
        'init': ['init'],
        'user': ['set-user'],
        'cookie': ['set-cookie'],
        'fetch': ['fetch'],
        'push': ['git-push'],
        'help': ['--help'],
        '-h': ['--help'],
        '--help': ['--help']
    }
    
    if command in command_map:
        if command in ['help', '-h', '--help']:
            show_help()
        else:
            run_command(command_map[command])
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Run 'lcsync help' to see available commands")
        sys.exit(1)

if __name__ == "__main__":
    main()