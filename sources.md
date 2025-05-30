# Class Action Lawsuit Sources

This document outlines the primary sources for finding class action lawsuits in the United States that require no proof to claim.

## Primary Sources

1. **Top Class Actions**
   - URL: https://topclassactions.com/category/lawsuit-settlements/open-lawsuit-settlements/
   - Features: Lists current open settlements, includes "no proof required" indicators
   - Update Frequency: Daily
   - Data Structure: Each settlement includes title, deadline, settlement amount, and claim submission link
   - Notes: One of the most comprehensive and regularly updated sources

2. **Lawsuit Update Center**
   - URL: https://www.lawsuitupdatecenter.com/no-proof-class-action-lawsuits-that-paid-money-recently.html
   - Features: Specifically focuses on no-proof-required settlements, includes detailed tables
   - Update Frequency: Weekly
   - Data Structure: Organized in tables with settlement name and claim deadline
   - Notes: Provides detailed breakdowns of settlement amounts and eligibility requirements

3. **Claim Depot**
   - URL: https://www.claimdepot.com/settlements
   - Features: Has specific "No Proof" filter and tags for applicable settlements
   - Update Frequency: Regular updates
   - Data Structure: Card-based layout with settlement details and status indicators
   - Notes: Includes filtering options specifically for "No Proof" settlements

## Data Extraction Strategy

For each source, the script will:
1. Access the website
2. Parse the HTML structure to identify settlement listings
3. Extract key information:
   - Settlement name/title
   - Claim deadline
   - Settlement amount (when available)
   - Whether proof is required (looking for "no proof" indicators)
   - Claim submission URL
4. Filter for settlements that explicitly require no proof
5. Store the data in a structured format for email notification

## Filtering Criteria

Settlements will be included in the notification if they meet the following criteria:
1. The settlement is currently open for claims
2. The settlement explicitly states "no proof required" or similar language
3. The settlement is available to US residents
4. The settlement has not been previously reported in earlier notifications
