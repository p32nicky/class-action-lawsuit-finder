#!/usr/bin/env python3
"""
Email Sender for Class Action Lawsuit Finder

This module handles the email notification functionality for the Class Action Lawsuit Finder app.
It uses SMTP to send formatted HTML emails with information about new class action lawsuits.

Author: Manus AI
Date: May 30, 2025
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional

# Configure logging
logger = logging.getLogger("email_sender")

def format_email_html(lawsuits: List[Dict[str, Any]]) -> str:
    """Format lawsuits as HTML for email"""
    if not lawsuits:
        return "<p>No new class action lawsuits requiring no proof were found today.</p>"
    
    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
            h2 { color: #3498db; margin-top: 20px; }
            .lawsuit { margin-bottom: 25px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            .lawsuit:hover { box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
            .deadline { color: #e74c3c; font-weight: bold; }
            .source { color: #7f8c8d; font-style: italic; font-size: 0.9em; margin-top: 15px; }
            a { color: #2980b9; text-decoration: none; font-weight: bold; }
            a:hover { text-decoration: underline; }
            .button { display: inline-block; background-color: #3498db; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; }
            .button:hover { background-color: #2980b9; text-decoration: none; }
            .footer { margin-top: 30px; padding-top: 15px; border-top: 1px solid #ddd; font-size: 0.9em; color: #7f8c8d; text-align: center; }
        </style>
    </head>
    <body>
        <h1>New Class Action Lawsuits - No Proof Required</h1>
        <p>Here are the latest class action lawsuits that require no proof to claim:</p>
    """
    
    for lawsuit in lawsuits:
        html += f"""
        <div class="lawsuit">
            <h2>{lawsuit["title"]}</h2>
            <p><span class="deadline">Deadline:</span> {lawsuit["deadline"]}</p>
            <p><a href="{lawsuit["link"]}" class="button" target="_blank">View Details & Submit Claim</a></p>
            <p class="source">Source: {lawsuit["source"]} (Found on {lawsuit["date_found"]})</p>
        </div>
        """
    
    html += """
        <div class="footer">
            <p>This email was sent by your automated Class Action Lawsuit Finder.</p>
            <p>To stop receiving these emails, update your GitHub Actions workflow.</p>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(recipient: str, subject: str, html_content: str, smtp_config: Dict[str, str]) -> bool:
    """
    Send email with the lawsuit information
    
    Args:
        recipient: Email address to send to
        subject: Email subject line
        html_content: HTML content of the email
        smtp_config: Dictionary containing SMTP configuration
            Required keys: server, port, username, password, from_email
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_config.get("from_email", smtp_config["username"])
        msg["To"] = recipient
        
        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        # Connect to SMTP server and send
        with smtplib.SMTP_SSL(smtp_config["server"], int(smtp_config["port"])) as server:
            server.login(smtp_config["username"], smtp_config["password"])
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {recipient}")
        return True
    
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def get_smtp_config_from_env() -> Dict[str, str]:
    """
    Get SMTP configuration from environment variables
    
    Environment variables used:
        - EMAIL_SMTP_SERVER: SMTP server address
        - EMAIL_SMTP_PORT: SMTP server port
        - EMAIL_USERNAME: SMTP username
        - EMAIL_PASSWORD: SMTP password
        - EMAIL_FROM: From email address (optional, defaults to username)
    
    Returns:
        Dict containing SMTP configuration
    """
    config = {
        "server": os.environ.get("EMAIL_SMTP_SERVER", ""),
        "port": os.environ.get("EMAIL_SMTP_PORT", "465"),  # Default to SSL port
        "username": os.environ.get("EMAIL_USERNAME", ""),
        "password": os.environ.get("EMAIL_PASSWORD", ""),
        "from_email": os.environ.get("EMAIL_FROM", "")
    }
    
    # Validate required fields
    missing_fields = [k for k, v in config.items() if not v and k != "from_email"]
    if missing_fields:
        logger.error(f"Missing required SMTP configuration: {', '.join(missing_fields)}")
        raise ValueError(f"Missing required SMTP configuration: {', '.join(missing_fields)}")
    
    # Use username as from_email if not specified
    if not config["from_email"]:
        config["from_email"] = config["username"]
    
    return config
