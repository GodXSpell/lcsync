"""
Init command implementation
Creates project folder structure and necessary files
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

import click


def check_and_install_requirements():
    """Check if required packages are installed and offer to install them"""
    logger = logging.getLogger()
    
    try:
        # Get project root directory
        project_root = Path.cwd()
        requirements_file = project_root / "requirements.txt"
        
        if not requirements_file.exists():
            click.echo("⚠️ requirements.txt not found. Will be created during initialization.")
            return True
        
        # Read requirements
        with open(requirements_file, 'r', encoding='utf-8') as f:
            requirements = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        
        if not requirements:
            click.echo("📦 No requirements found in requirements.txt")
            return True
        
        # Check which packages are missing
        missing_packages = []
        installed_packages = []
        
        for requirement in requirements:
            package_name = requirement.split('>=')[0].split('==')[0].split('<')[0].strip()
            try:
                __import__(package_name)
                installed_packages.append(package_name)
                logger.info(f"Package '{package_name}' is already installed")
            except ImportError:
                missing_packages.append(requirement)
                logger.warning(f"Package '{package_name}' is missing")
        
        # Display status
        if installed_packages:
            click.echo(f"✅ Already installed: {', '.join(installed_packages)}")
        
        if not missing_packages:
            click.echo("🎉 All required packages are already installed!")
            return True
        
        # Ask user for confirmation to install missing packages
        click.echo(f"\n📦 Missing packages: {', '.join([pkg.split('>=')[0].split('==')[0] for pkg in missing_packages])}")
        
        if click.confirm("Would you like to install the missing packages now?", default=True):
            return install_requirements(missing_packages)
        else:
            click.echo("⚠️ Skipping package installation. You may need to install them manually later:")
            click.echo(f"   pip install {' '.join(missing_packages)}")
            return False
            
    except Exception as e:
        error_msg = f"Error checking requirements: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        return False


def install_requirements(packages_to_install):
    """Install the specified packages using pip"""
    logger = logging.getLogger()
    
    try:
        click.echo("🔄 Installing packages...")
        
        # Prepare pip install command
        cmd = [sys.executable, "-m", "pip", "install"] + packages_to_install
        
        # Run pip install
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            click.echo("✅ Successfully installed all packages!")
            logger.info(f"Successfully installed packages: {', '.join(packages_to_install)}")
            return True
        else:
            error_msg = f"Failed to install packages. Error: {result.stderr}"
            click.echo(f"❌ {error_msg}", err=True)
            logger.error(error_msg)
            click.echo("\n💡 Try installing manually:")
            click.echo(f"   pip install {' '.join(packages_to_install)}")
            return False
            
    except Exception as e:
        error_msg = f"Error during package installation: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        click.echo("\n💡 Try installing manually:")
        click.echo(f"   pip install {' '.join(packages_to_install)}")
        return False


def init_project():
    """Initialize project folders and .gitignore"""
    logger = logging.getLogger()
    
    try:
        click.echo("🚀 Initializing LeetCode Sync project...")
        
        # Step 1: Check and install requirements
        click.echo("\n📦 Step 1: Checking Python dependencies...")
        deps_success = check_and_install_requirements()
        
        if not deps_success:
            click.echo("\n⚠️ Some dependencies may be missing, but continuing with initialization...")
        
        # Step 2: Create tool structure
        click.echo("\n📁 Step 2: Creating tool structure...")
        
        # Get project root directory (tool directory)
        project_root = Path.cwd()
        
        # Create directory structure (only tool-related directories)
        directories = [
            project_root / "users",
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
        
        # Only create requirements.txt if it doesn't exist
        if not requirements_file.exists():
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
        
        # Summary
        click.echo("\n✅ Tool initialized successfully!")
        click.echo("Created directories:")
        for directory in directories:
            click.echo(f"  📁 {directory.relative_to(project_root)}")
        
        click.echo("\nCreated files:")
        click.echo(f"  📄 {users_gitignore.relative_to(project_root)}")
        click.echo(f"  📄 {log_file.relative_to(project_root)}")
        if not requirements_file.exists():
            click.echo(f"  📄 {requirements_file.relative_to(project_root)}")
        click.echo(f"  📄 {main_gitignore.relative_to(project_root)}")
        
        if deps_success:
            click.echo("\n🎉 All dependencies are ready!")
        else:
            click.echo("\n⚠️ Please install missing dependencies manually if needed")
        
        click.echo("\n🚀 Next step: Run 'lcsync user' to set up your target repository")
        click.echo("💡 The 'lcsync user' command will create the leetcodeProblems folder in your chosen repository directory")
        
    except Exception as e:
        error_msg = f"Failed to initialize project: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)