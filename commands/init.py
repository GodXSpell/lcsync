"""
Init command implementation
Creates project folder structure and necessary files
"""

import logging
import os
from pathlib import Path

import click


def init_project():
    """Initialize project folders and .gitignore"""
    logger = logging.getLogger()
    
    try:
        # Get project root directory
        project_root = Path.cwd()
        
        # Create directory structure
        directories = [
            project_root / "users",
            project_root / "leetcodeProblems" / "easy",
            project_root / "leetcodeProblems" / "medium", 
            project_root / "leetcodeProblems" / "hard",
            project_root / "commands"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        
        # Create .gitignore in users/ directory to ignore all contents
        users_gitignore = project_root / "users" / ".gitignore"
        gitignore_content = """# Ignore all user data files (contains sensitive cookies)
*
!.gitignore
"""
        
        with open(users_gitignore, 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        logger.info(f"Created .gitignore in users/ directory")
        
        # Create empty log file in project root
        log_file = project_root / "leetcode_auto_push.log"
        if not log_file.exists():
            log_file.touch()
            logger.info(f"Created log file: {log_file}")
        
        # Create requirements.txt for dependencies
        requirements_file = project_root / "requirements.txt"
        requirements_content = """click>=8.0.0
requests>=2.25.0
"""
        
        with open(requirements_file, 'w', encoding='utf-8') as f:
            f.write(requirements_content)
        logger.info(f"Created requirements.txt")
        
        # Create main .gitignore for the project
        main_gitignore = project_root / ".gitignore"
        main_gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# User data (sensitive information)
users/
!users/.gitignore

# Logs
*.log
"""
        
        with open(main_gitignore, 'w', encoding='utf-8') as f:
            f.write(main_gitignore_content)
        logger.info(f"Created main .gitignore")
        
        click.echo("✅ Project initialized successfully!")
        click.echo("Created directories:")
        for directory in directories:
            click.echo(f"  📁 {directory.relative_to(project_root)}")
        
        click.echo("\nCreated files:")
        click.echo(f"  📄 {users_gitignore.relative_to(project_root)}")
        click.echo(f"  📄 {log_file.relative_to(project_root)}")
        click.echo(f"  📄 {requirements_file.relative_to(project_root)}")
        click.echo(f"  📄 {main_gitignore.relative_to(project_root)}")
        
        click.echo("\n🚀 Next step: Run 'python leetcode_auto_push.py set_user' to configure your user settings")
        
    except Exception as e:
        error_msg = f"Failed to initialize project: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)