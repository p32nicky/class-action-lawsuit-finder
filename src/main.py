#!/usr/bin/env python3
"""
Class Action Lawsuit Finder

This script searches for new class action lawsuits in the United States that require no proof to claim
and emails the results to the specified recipient.

Author: Manus AI
Date: May 30, 2025
"""

import os
import json
import logging
import datetime
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from email_sender import format_email_html, send_email, get_smtp_config_from_env

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("class_action_finder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("class_action_finder")

# Constants
DATA_FILE = "previous_lawsuits.json"
EMAIL_RECIPIENT = os.environ.get("EMAIL_RECIPIENT", "nickdavies100@gmail.com")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


class LawsuitFinder:
    """Base class for lawsuit finders"""
    
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        }
    
    def fetch_page(self) -> Optional[str]:
        """Fetch the HTML content of the page"""
        try:
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {self.name}: {e}")
            return None
    
    def parse_lawsuits(self, html: str) -> List[Dict[str, Any]]:
        """Parse the HTML to extract lawsuit information"""
        raise NotImplementedError("Subclasses must implement parse_lawsuits")
    
    def get_lawsuits(self) -> List[Dict[str, Any]]:
        """Get lawsuits from the source"""
        html = self.fetch_page()
        if not html:
            return []
        
        lawsuits = self.parse_lawsuits(html)
        for lawsuit in lawsuits:
            lawsuit["source"] = self.name
            lawsuit["date_found"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        return lawsuits


class TopClassActionsFinder(LawsuitFinder):
    """Finder for Top Class Actions website"""
    
    def parse_lawsuits(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        lawsuits = []
        
        # Find all settlement entries
        settlement_entries = soup.find_all("article", class_="settlement-card")
        
        for entry in settlement_entries:
            try:
                # Extract title
                title_element = entry.find("h2", class_="settlement-title")
                if not title_element:
                    continue
                title = title_element.text.strip()
                
                # Extract deadline
                deadline_element = entry.find("div", class_="settlement-deadline")
                deadline = deadline_element.text.strip() if deadline_element else "Unknown"
                
                # Extract link
                link_element = entry.find("a", class_="settlement-link")
                link = link_element["href"] if link_element else ""
                
                # Check if no proof is required
                description = entry.find("div", class_="settlement-description")
                description_text = description.text.lower() if description else ""
                no_proof_required = any(term in description_text for term in [
                    "no proof", "no receipt", "without proof", "without receipt"
                ])
                
                if no_proof_required:
                    lawsuits.append({
                        "title": title,
                        "deadline": deadline,
                        "link": link,
                        "no_proof_required": True
                    })
            except Exception as e:
                logger.error(f"Error parsing Top Class Actions entry: {e}")
        
        return lawsuits


class LawsuitUpdateCenterFinder(LawsuitFinder):
    """Finder for Lawsuit Update Center website"""
    
    def parse_lawsuits(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        lawsuits = []
        
        # This page is specifically for no-proof lawsuits, so all entries qualify
        try:
            # Find the table with settlements
            table = soup.find("table")
            if not table:
                return lawsuits
            
            rows = table.find_all("tr")
            # Skip header row
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    title = cells[0].text.strip()
                    deadline = cells[1].text.strip()
                    
                    lawsuits.append({
                        "title": title,
                        "deadline": deadline,
                        "link": self.url,  # Use the main page as link since individual links aren't available
                        "no_proof_required": True
                    })
        except Exception as e:
            logger.error(f"Error parsing Lawsuit Update Center: {e}")
        
        return lawsuits


class ClaimDepotFinder(LawsuitFinder):
    """Finder for Claim Depot website"""
    
    def parse_lawsuits(self, html: str) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        lawsuits = []
        
        try:
            # Find all settlement cards
            settlement_cards = soup.find_all("div", class_="settlement-card")
            
            for card in settlement_cards:
                # Check if it has a "No Proof" tag
                no_proof_tag = card.find("span", class_="no-proof-tag")
                
                if no_proof_tag:
                    title_element = card.find("h3", class_="settlement-title")
                    title = title_element.text.strip() if title_element else "Unknown Settlement"
                    
                    deadline_element = card.find("div", class_="deadline")
                    deadline = deadline_element.text.strip() if deadline_element else "Unknown"
                    
                    link_element = card.find("a", class_="settlement-link")
                    link = link_element["href"] if link_element else ""
                    
                    lawsuits.append({
                        "title": title,
                        "deadline": deadline,
                        "link": link,
                        "no_proof_required": True
                    })
        except Exception as e:
            logger.error(f"Error parsing Claim Depot: {e}")
        
        return lawsuits


def load_previous_lawsuits() -> List[Dict[str, Any]]:
    """Load previously found lawsuits from file"""
    if not os.path.exists(DATA_FILE):
        return []
    
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading previous lawsuits: {e}")
        return []


def save_lawsuits(lawsuits: List[Dict[str, Any]]) -> None:
    """Save lawsuits to file"""
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(lawsuits, f, indent=2)
    except IOError as e:
        logger.error(f"Error saving lawsuits: {e}")


def filter_new_lawsuits(current: List[Dict[str, Any]], previous: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filter out lawsuits that were already found"""
    previous_titles = {lawsuit["title"] for lawsuit in previous}
    return [lawsuit for lawsuit in current if lawsuit["title"] not in previous_titles]


def main():
    """Main function to run the lawsuit finder"""
    logger.info("Starting Class Action Lawsuit Finder")
    
    # Initialize finders
    finders = [
        TopClassActionsFinder(
            "Top Class Actions",
            "https://topclassactions.com/category/lawsuit-settlements/open-lawsuit-settlements/"
        ),
        LawsuitUpdateCenterFinder(
            "Lawsuit Update Center",
            "https://www.lawsuitupdatecenter.com/no-proof-class-action-lawsuits-that-paid-money-recently.html"
        ),
        ClaimDepotFinder(
            "Claim Depot",
            "https://www.claimdepot.com/settlements"
        )
    ]
    
    # Load previous lawsuits
    previous_lawsuits = load_previous_lawsuits()
    logger.info(f"Loaded {len(previous_lawsuits)} previously found lawsuits")
    
    # Get current lawsuits from all sources
    all_lawsuits = []
    for finder in finders:
        logger.info(f"Fetching lawsuits from {finder.name}")
        lawsuits = finder.get_lawsuits()
        logger.info(f"Found {len(lawsuits)} lawsuits from {finder.name}")
        all_lawsuits.extend(lawsuits)
    
    # Filter for new lawsuits
    new_lawsuits = filter_new_lawsuits(all_lawsuits, previous_lawsuits)
    logger.info(f"Found {len(new_lawsuits)} new lawsuits")
    
    if new_lawsuits:
        # Format email
        html_content = format_email_html(new_lawsuits)
        
        # Send email
        subject = f"New Class Action Lawsuits - No Proof Required ({datetime.datetime.now().strftime('%Y-%m-%d')})"
        
        try:
            # Get SMTP configuration from environment variables
            smtp_config = get_smtp_config_from_env()
            
            # Send email
            success = send_email(EMAIL_RECIPIENT, subject, html_content, smtp_config)
            
            if success:
                logger.info("Email sent successfully")
                
                # Save all lawsuits for future reference
                all_lawsuits_to_save = previous_lawsuits + new_lawsuits
                save_lawsuits(all_lawsuits_to_save)
                logger.info(f"Saved {len(all_lawsuits_to_save)} lawsuits to file")
            else:
                logger.error("Failed to send email")
        except ValueError as e:
            logger.error(f"Email configuration error: {e}")
            logger.info("Saving lawsuits anyway to prevent duplicate notifications next run")
            all_lawsuits_to_save = previous_lawsuits + new_lawsuits
            save_lawsuits(all_lawsuits_to_save)
    else:
        logger.info("No new lawsuits found")
    
    logger.info("Class Action Lawsuit Finder completed")


if __name__ == "__main__":
    main()
