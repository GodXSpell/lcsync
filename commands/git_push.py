"""
Git push command implementation
Bundle git add, commit, push operations
"""

import logging
import os
import subprocess
from pathlib import Path

import click

from .set_user import get_user_config


def git_push(custom_message=None):
    """Bundle git add, commit, push operations"""
    logger = logging.getLogger()
    
    try:
        # Get user configuration
        username, config = get_user_config()
        
        repo_path = Path(config["GITHUB_REPO_DIR"])
        
        # Use custom message if provided, otherwise use default from config
        if custom_message:
            commit_message = custom_message
        else:
            commit_message = config["GITHUB_COMMIT_MESSAGE"]
        
        click.echo(f"🚀 Git operations for user: {username}")
        click.echo(f"📁 Repository: {repo_path}")
        click.echo(f"💬 Commit message: {commit_message}")
        click.echo()
        
        # Validate repository path
        if not repo_path.exists():
            raise click.ClickException(f"Repository path does not exist: {repo_path}")
        
        git_dir = repo_path / ".git"
        if not git_dir.exists():
            raise click.ClickException(f"Not a Git repository: {repo_path}")
        
        # Change to repository directory
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        try:
            # Step 1: git add .
            click.echo("📝 Running: git add .")
            result = subprocess.run(
                ["git", "add", "."],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = f"git add failed: {result.stderr}"
                logger.error(error_msg)
                raise click.ClickException(error_msg)
            
            logger.info("git add completed successfully")
            click.echo("✅ git add completed")
            
            # Check if there are any changes to commit
            result = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                click.echo("ℹ️  No changes to commit")
                logger.info("No changes to commit")
                return
            
            # Step 2: git commit
            click.echo(f"💾 Running: git commit -m \"{commit_message}\"")
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = f"git commit failed: {result.stderr}"
                logger.error(error_msg)
                raise click.ClickException(error_msg)
            
            logger.info(f"git commit completed: {commit_message}")
            click.echo("✅ git commit completed")
            
            # Step 3: git push
            click.echo("🚀 Running: git push")
            result = subprocess.run(
                ["git", "push"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = f"git push failed: {result.stderr}"
                logger.error(error_msg)
                
                # Provide helpful error messages
                if "fatal: unable to access" in result.stderr.lower():
                    error_msg += "\n\n💡 Possible solutions:"
                    error_msg += "\n   • Check your internet connection"
                    error_msg += "\n   • Verify your Git credentials (SSH key or token)"
                    error_msg += "\n   • Run 'git remote -v' to check remote URL"
                elif "fatal: the current branch" in result.stderr.lower():
                    error_msg += "\n\n💡 Try: git push --set-upstream origin main"
                elif "permission denied" in result.stderr.lower():
                    error_msg += "\n\n💡 Check your Git authentication (SSH key or token)"
                
                raise click.ClickException(error_msg)
            
            logger.info("git push completed successfully")
            click.echo("✅ git push completed")
            
            click.echo()
            click.echo("🎉 All Git operations completed successfully!")
            
        finally:
            # Always restore original working directory
            os.chdir(original_cwd)
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Git command failed: {e}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)
    except Exception as e:
        error_msg = f"Git operations failed: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)

def check_git_status(repo_path):
    """Check git status and return info about uncommitted changes"""
    try:
        original_cwd = os.getcwd()
        os.chdir(repo_path)
        
        try:
            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            if lines:
                return {
                    "has_changes": True,
                    "num_changes": len(lines),
                    "changes": lines
                }
            else:
                return {"has_changes": False, "num_changes": 0, "changes": []}
                
        finally:
            os.chdir(original_cwd)
            
    except subprocess.CalledProcessError:
        return {"has_changes": False, "num_changes": 0, "changes": [], "error": True}