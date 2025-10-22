# Gradescope Analysis and Email System

A Python tool for analyzing student performance from Gradescope CSV exports and sending personalized encouraging emails based on performance trends.

## Features

- **Performance Analysis**: Analyzes student performance across multiple quizzes
- **Student Categorization**: Automatically categorizes students into:
  - **Excelling**: High scores on both quizzes
  - **Improving**: Low on quiz 2, high on quiz 3
  - **Struggling**: Low scores on both quizzes
  - **Declining**: High on quiz 2, low on quiz 3
  - **Consistent**: Similar performance on both quizzes
- **Personalized Emails**: Sends encouraging messages tailored to each student's performance
- **University Email Support**: Configured for UNC and other university email systems
- **Dry Run Mode**: Preview emails before sending

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare Your Data**:
   - Export your Gradescope data as CSV files
   - Name them `three-scores.csv` and `two-scores.csv` (or modify the script)
   - Ensure the CSV files have columns: Name, Email, Total Score, Max Points

3. **Run the Analysis**:
   ```bash
   python demo_analysis.py
   ```

## Usage

### Basic Analysis (No Emails)
```bash
python demo_analysis.py
```

### Full Analysis with Email Options
```bash
python gradescope_analyzer.py
```

### Test Email Functionality
```bash
# Quick test with UNC settings
python quick_email_test.py

# Full test with multiple email providers
python test_email.py
```

### Email Configuration

The system supports multiple email providers:

#### UNC Chapel Hill (Office 365)
- SMTP Server: `smtp.office365.com`
- Port: `587`
- Use your UNC email and password

#### Gmail
- SMTP Server: `smtp.gmail.com`
- Port: `587`
- Requires app password (not regular password)

#### Other Universities
- Check your university's IT documentation for SMTP settings
- Common ports: 587 (TLS) or 465 (SSL)

## File Structure

```
311-proj/
├── gradescope_analyzer.py    # Main analysis and email system
├── demo_analysis.py          # Safe demo without sending emails
├── test_email.py             # Full email testing with multiple providers
├── quick_email_test.py       # Quick email test with UNC settings
├── email_config.py           # Email configuration for universities
├── requirements.txt          # Python dependencies
├── three-scores.csv         # Gradescope data (Quiz 3)
├── two-scores.csv           # Gradescope data (Quiz 2)
└── README.md                # This file
```

## Email Templates

The system includes personalized email templates for each student category:

- **Excelling Students**: Recognition for consistent high performance
- **Improving Students**: Congratulations on improvement with specific metrics
- **Struggling Students**: Supportive message with offers of help
- **Declining Students**: Concerned but supportive message
- **Consistent Students**: Acknowledgment of steady progress

## Security Notes

- Never hardcode passwords in your code
- Use environment variables for sensitive information
- Consider using OAuth2 for better security
- Always test with dry run mode first

## Example Output

```
GRADESCOPE PERFORMANCE ANALYSIS REPORT
=====================================
Generated on: 2025-01-27 10:30:00

Total Students Analyzed: 150

EXCELLING STUDENTS (45 students):
----------------------------------------
• John Doe (john@unc.edu)
  Quiz 2: 95.0%
  Quiz 3: 92.0%

IMPROVING STUDENTS (23 students):
----------------------------------------
• Jane Smith (jane@unc.edu)
  Quiz 2: 75.0%
  Quiz 3: 88.0%
  Improvement: +13.0%
```

## Troubleshooting

### Common Issues

1. **CSV File Not Found**: Ensure your CSV files are in the same directory as the script
2. **Email Authentication Failed**: Check your email credentials and SMTP settings
3. **Permission Denied**: Some universities require specific authentication methods

### Getting Help

- Check your university's IT documentation for email settings
- Test with dry run mode first
- Verify CSV file format matches expected columns

## License

This project is for educational use. Please ensure compliance with your institution's policies regarding student data and email communications.
