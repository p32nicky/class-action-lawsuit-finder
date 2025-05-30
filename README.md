# Class Action Lawsuit Finder

This application automatically searches for new class action lawsuits in the United States that require no proof to claim and emails the results to you daily.

## Features

- Scans multiple reputable sources for class action lawsuit settlements
- Filters for settlements that specifically require no proof to claim
- Sends beautifully formatted HTML emails with settlement details
- Tracks previously found lawsuits to avoid duplicate notifications
- Designed to run daily via GitHub Actions

## Sources

The application searches the following sources:

1. [Top Class Actions](https://topclassactions.com/)
2. [Lawsuit Update Center](https://www.lawsuitupdatecenter.com/)
3. [Claim Depot](https://www.claimdepot.com/)

## Setup Instructions

### 1. Fork or Clone this Repository

Start by forking this repository to your GitHub account or cloning it to create your own repository.

### 2. Configure Email Settings

You'll need to set up the following GitHub Secrets in your repository to enable email notifications:

1. Go to your repository on GitHub
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Add the following secrets:

| Secret Name | Description |
|-------------|-------------|
| `EMAIL_SMTP_SERVER` | Your SMTP server address (e.g., `smtp.gmail.com`) |
| `EMAIL_SMTP_PORT` | SMTP port (typically `465` for SSL or `587` for TLS) |
| `EMAIL_USERNAME` | Your email username/address |
| `EMAIL_PASSWORD` | Your email password or app password |
| `EMAIL_RECIPIENT` | Email address to receive notifications (default: nickdavies100@gmail.com) |

#### Using Gmail

If you're using Gmail, you'll need to create an "App Password":

1. Go to your Google Account settings
2. Select "Security"
3. Under "Signing in to Google," select "2-Step Verification" (must be enabled)
4. At the bottom, select "App passwords"
5. Create a new app password for "Mail" and "Other (Custom name)"
6. Use this generated password for `EMAIL_PASSWORD`

### 3. Enable GitHub Actions

The repository includes a GitHub Actions workflow file that runs the script daily:

1. In your repository, go to the "Actions" tab
2. Click "I understand my workflows, go ahead and enable them"

## How It Works

1. The script runs daily via GitHub Actions
2. It checks multiple sources for class action lawsuits requiring no proof
3. New lawsuits (not previously found) are compiled into an HTML email
4. The email is sent to your specified email address
5. Found lawsuits are saved to avoid duplicate notifications

## Customization

### Changing Email Recipient

By default, emails are sent to the address specified in the `EMAIL_RECIPIENT` secret. You can change this in the GitHub repository secrets.

### Modifying Sources

If you want to add or remove sources, edit the `main.py` file:

```python
# Initialize finders
finders = [
    TopClassActionsFinder(
        "Top Class Actions",
        "https://topclassactions.com/category/lawsuit-settlements/open-lawsuit-settlements/"
    ),
    # Add or remove sources here
]
```

### Changing Email Format

To modify the email format, edit the `format_email_html` function in `email_sender.py`.

## GitHub Actions Workflow

The included `.github/workflows/daily-check.yml` file configures GitHub Actions to run the script daily. You can modify the schedule by editing the cron expression in this file.

Default schedule: Runs daily at 8:00 AM UTC.

## Local Development

To run the script locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables for email configuration:
   ```
   export EMAIL_SMTP_SERVER=your_smtp_server
   export EMAIL_SMTP_PORT=your_smtp_port
   export EMAIL_USERNAME=your_email
   export EMAIL_PASSWORD=your_password
   export EMAIL_RECIPIENT=recipient_email
   ```
4. Run the script: `python src/main.py`

## Troubleshooting

### Email Not Sending

- Check that all email secrets are correctly configured in GitHub
- Verify your SMTP settings (server, port)
- For Gmail, ensure you're using an App Password if 2FA is enabled
- Check the GitHub Actions logs for error messages

### No Lawsuits Found

- The script only notifies about new lawsuits not previously found
- Check the GitHub Actions logs to see if any lawsuits were found but were not new
- The sources might not have updated with new lawsuits

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for informational purposes only. It does not provide legal advice, and the creators are not responsible for the accuracy of the information provided by the sources. Always verify eligibility requirements before submitting claims.
