#!/usr/bin/env python3
"""
LeetCode Submission Auto GitHub Push CLI
A professional tool to automatically fetch and organize LeetCode submissions.
"""

import logging
import os
from pathlib import Path

import click

# Commands will be imported within each command function to avoid conflicts

# Set up logging
def setup_logging():
    """Configure logging to file and console"""
    log_file = Path(__file__).parent / "leetcode_auto_push.log"
    
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

@click.group()
@click.version_option(version="1.0.0", prog_name="LeetCode Auto Push")
def cli():
    """
    LeetCode Submission Auto GitHub Push CLI
    
    Automatically fetch and organize your LeetCode submissions,
    then optionally push them to GitHub.
    """
    setup_logging()

@cli.command()
def init():
    """Initialize project folders and .gitignore"""
    from commands.init import init_project
    init_project()

@cli.command()
def set_user():
    """One-time user setup (username, GitHub repo, commit message)"""
    from commands.set_user import set_user as set_user_func
    set_user_func()

@cli.command()
def set_cookie():
    """Update/change LeetCode session cookie"""
    from commands.set_cookie import set_cookie as set_cookie_func
    set_cookie_func()

@cli.command()
def fetch():
    """Fetch new accepted submissions from LeetCode"""
    from commands.fetch import fetch_submissions
    fetch_submissions()

@cli.command()
@click.option('-m', '--message', help='Custom commit message')
def git_push(message):
    """Bundle git add, commit, push operations"""
    from commands.git_push import git_push as git_push_func
    git_push_func(message)

if __name__ == "__main__":
    cli()