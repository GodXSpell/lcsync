"""
Set cookie command implementation
Update/change LeetCode session cookie
"""

import logging

import click

from .set_user import get_user_config, save_user_config


def set_cookie():
    """Update/change LeetCode session cookie"""
    logger = logging.getLogger()
    
    try:
        # Get user configuration
        username, config = get_user_config()
        
        click.echo(f"🔑 Updating LeetCode session cookie for user: {username}")
        click.echo()
        click.echo("To get your session cookie:")
        click.echo("1. Go to leetcode.com and log in")
        click.echo("2. Open browser developer tools (F12)")
        click.echo("3. Go to Application/Storage > Cookies > https://leetcode.com")
        click.echo("4. Find the 'LEETCODE_SESSION' or 'csrftoken' cookie value")
        click.echo("5. Copy the entire cookie string")
        click.echo()
        
        # Get current cookie status
        current_cookie = config.get("LEETCODE_COOKIE", "")
        if current_cookie:
            masked_cookie = current_cookie[:10] + "..." + current_cookie[-10:] if len(current_cookie) > 20 else current_cookie
            click.echo(f"Current cookie: {masked_cookie}")
        else:
            click.echo("Current cookie: Not set")
        
        click.echo()
        
        # Prompt for new cookie
        new_cookie = click.prompt(
            "Enter new LeetCode session cookie", 
            type=str,
            hide_input=True  # Hide the cookie input for security
        ).strip()
        
        if not new_cookie:
            raise click.ClickException("Cookie cannot be empty")
        
        # Basic validation - cookies are typically long strings
        if len(new_cookie) < 10:
            click.echo("⚠️  Warning: Cookie seems unusually short")
            if not click.confirm("Continue anyway?"):
                raise click.ClickException("Cookie update cancelled")
        
        # Update configuration
        config["LEETCODE_COOKIE"] = new_cookie
        save_user_config(username, config)
        
        logger.info(f"Updated LeetCode session cookie for user: {username}")
        
        click.echo()
        click.echo("✅ LeetCode session cookie updated successfully!")
        click.echo()
        click.echo("🚀 Next step: Run 'python leetcode_auto_push.py fetch' to fetch your submissions")
        
    except Exception as e:
        error_msg = f"Failed to update cookie: {str(e)}"
        logger.error(error_msg)
        click.echo(f"❌ {error_msg}", err=True)
        raise click.ClickException(error_msg)