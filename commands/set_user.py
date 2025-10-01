"""
Set user command implementation
One-time user setup for username, GitHub repo, and commit message
"""

import json
import logging
import os
from pathlib import Path

import click


def set_user():
    """One-time user setup (username, GitHub repo, commit message)"""
    logger = logging.getLogger()
    
    try:
        # Get project root and users directory
        project_root = Path.cwd()
        users_dir = project_root / "users"
        
        # Ensure users directory exists
        if not users_dir.exists():
            click.echo("❌ Users directory not found. Please run 'init' command first.")
            raise click.ClickException("Project not initialized")
        
        # Interactive prompts
        click.echo("🚀 Setting up user configuration...")
        click.echo()
        
        username = click.prompt("Enter username", type=str).strip()
        if not username:
            raise click.ClickException("Username cannot be empty")
        
        github_repo_path = click.prompt("Enter local GitHub repo path", type=str).strip()
        if not github_repo_path:
            raise click.ClickException("GitHub repo path cannot be empty")
        
        # Validate that the path exists
        repo_path = Path(github_repo_path).expanduser().resolve()
        if not repo_path.exists():
            click.echo(f"⚠️  Warning: Path '{repo_path}' does not exist")
            if not click.confirm("Continue anyway?"):
                raise click.ClickException("Setup cancelled")
        
        # Check if it's a git repository
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            click.echo(f"⚠️  Warning: '{repo_path}' does not appear to be a Git repository")
            if not click.confirm("Continue anyway?"):
                raise click.ClickException("Setup cancelled")
        
        commit_message = click.prompt(
            "Enter commit message", 
            default="Update LeetCode submissions",
            type=str
        ).strip()
        
        # Create LeetCode directory structure in the target repository
        click.echo(f"\n📁 Creating LeetCode directory structure in {repo_path}...")
        leetcode_directories = [
            repo_path / "leetcodeProblems" / "easy",
            repo_path / "leetcodeProblems" / "medium", 
            repo_path / "leetcodeProblems" / "hard"
        ]
        
        for directory in leetcode_directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        
        click.echo("✅ Created LeetCode directory structure:")
        for directory in leetcode_directories:
            relative_path = directory.relative_to(repo_path)
            click.echo(f"  📁 {relative_path}")
        
        # Create user configuration
        user_config = {
            "LEETCODE_COOKIE": "",  # Will be set later with set_cookie command
            "GITHUB_REPO_DIR": str(repo_path),
            "GITHUB_COMMIT_MESSAGE": commit_message
        }
        
        # Save user configuration
        user_file = users_dir / f"{username}.json"
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_config, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Created user configuration for: {username}")
        logger.info(f"GitHub repo path: {repo_path}")
        logger.info(f"Commit message: {commit_message}")
        
        click.echo()
        click.echo("✅ User configuration saved successfully!")
        click.echo(f"📁 User file: {user_file.relative_to(project_root)}")
        click.echo(f"📁 LeetCode solutions will be saved to: {repo_path / 'leetcodeProblems'}")
        click.echo()
        click.echo("🔑 Next step: Run 'lcsync cookie' to add your LeetCode session cookie")
        
    except Exception as e:
        error_msg = f"Failed to set user configuration: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)

def get_user_config(username=None):
    """
    Get user configuration. If username not provided, try to find a single user config.
    Returns tuple: (username, config_dict)
    """
    project_root = Path.cwd()
    users_dir = project_root / "users"
    
    if not users_dir.exists():
        raise click.ClickException("Users directory not found. Please run 'init' command first.")
    
    # Find user config files
    user_files = list(users_dir.glob("*.json"))
    
    if not user_files:
        raise click.ClickException("No user configurations found. Please run 'set_user' command first.")
    
    if username:
        # Look for specific user
        user_file = users_dir / f"{username}.json"
        if not user_file.exists():
            raise click.ClickException(f"User configuration not found for: {username}")
        actual_username = username
    else:
        # Auto-detect single user
        if len(user_files) == 1:
            user_file = user_files[0]
            actual_username = user_file.stem
        else:
            usernames = [f.stem for f in user_files]
            click.echo("Multiple users found:")
            for i, name in enumerate(usernames, 1):
                click.echo(f"  {i}. {name}")
            choice = click.prompt("Select user number", type=int)
            if choice < 1 or choice > len(usernames):
                raise click.ClickException("Invalid selection")
            actual_username = usernames[choice - 1]
            user_file = users_dir / f"{actual_username}.json"
    
    # Load and return config
    try:
        with open(user_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return actual_username, config
    except Exception as e:
        raise click.ClickException(f"Failed to load user configuration: {str(e)}")

def save_user_config(username, config):
    """Save user configuration to file"""
    project_root = Path.cwd()
    users_dir = project_root / "users"
    user_file = users_dir / f"{username}.json"
    
    try:
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise click.ClickException(f"Failed to save user configuration: {str(e)}")