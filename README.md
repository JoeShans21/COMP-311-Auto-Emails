# Gradescope Analysis and Email System (Gmail Version)

A Python tool for analyzing student performance from Gradescope CSV exports and sending personalized encouraging emails via Gmail based on performance trends.

## Features

- **Performance Analysis**: Analyzes student performance across multiple quizzes
- **Smart Student Categorization**: Automatically categorizes students into:
  - **Excelling**: High scores on both quizzes (≥85%)
  - **Improving**: Significant improvement (15+ points) OR low Quiz 2 but good Quiz 3
  - **Struggling**: Low scores on both quizzes (<60%)
  - **Declining**: High Quiz 2 but low Quiz 3 (≥75% → <60%)
  - **Consistent**: Similar performance or moderate changes
- **Personalized Emails**: Sends encouraging messages tailored to each student's performance
- **Gmail Integration**: Uses Gmail SMTP for reliable email delivery
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

3. **Gmail Setup** (Required for sending emails):
   - Enable 2-Factor Authentication on your Gmail account
   - Generate an App Password:
     - Go to: https://myaccount.google.com/security
     - Click '2-Step Verification' → 'App passwords'
     - Generate password for 'Mail'

## Usage

### Basic Analysis (No Emails)
```bash
python demo_analysis.py
```

### Full Analysis with Gmail Integration
```bash
python gradescope_analyzer.py
```

### Gmail Configuration

The system uses Gmail for reliable email delivery:

- **SMTP Server**: `smtp.gmail.com`
- **Port**: `587`
- **Authentication**: Gmail App Password (not regular password)
- **Setup**: Requires 2-Factor Authentication enabled

## File Structure

```
COMP-311-Auto-Emails/
├── gradescope_analyzer.py    # Main analysis and Gmail email system
├── demo_analysis.py          # Safe demo without sending emails
├── gmail_test.py             # Gmail email testing
├── requirements.txt          # Python dependencies
├── three-scores.csv         # Gradescope data (Quiz 3)
├── two-scores.csv           # Gradescope data (Quiz 2)
├── gradescope_analysis_*.json # Generated analysis reports
└── README.md                # This file
```

## Email Templates

The system includes personalized email templates for each student category:

- **Excelling Students**: Recognition for consistent high performance (≥85% on both quizzes)
- **Improving Students**: Congratulations on significant improvement with specific metrics
- **Struggling Students**: Supportive message with offers of help (both scores <60%)
- **Declining Students**: Concerned but supportive message (high Quiz 2, low Quiz 3)
- **Consistent Students**: Acknowledgment of steady progress

## Security Notes

- Never hardcode passwords in your code
- Use Gmail App Passwords (not regular passwords)
- Always test with dry run mode first
- Gmail App Passwords are more secure than regular passwords

## Example Output

```
GRADESCOPE PERFORMANCE ANALYSIS REPORT
=====================================
Generated on: 2025-01-27 10:30:00

Total Students Analyzed: 160

IMPROVING STUDENTS (30 students):
----------------------------------------
• Neha Bharadwaj (nehab4@ad.unc.edu)
  Quiz 2: 56.0%
  Quiz 3: 84.0%
  Improvement: +28.0%

• Zabdiel Villalobos (zabdielv@unc.edu)
  Quiz 2: 0.0%
  Quiz 3: 74.0%

DECLINING STUDENTS (4 students):
----------------------------------------
• Rachel Alvis (rcalvis@unc.edu)
  Quiz 2: 77.0%
  Quiz 3: 36.0%

CONSISTENT STUDENTS (26 students):
----------------------------------------
• Mann Barot (manbar@unc.edu)
  Quiz 2: 89.0%
  Quiz 3: 84.0%
```

## Troubleshooting

### Common Issues

1. **CSV File Not Found**: Ensure your CSV files are in the same directory as the script
2. **Gmail Authentication Failed**: 
   - Ensure 2-Factor Authentication is enabled
   - Use App Password (not regular password)
   - Check that "Less secure app access" is not the issue (use App Passwords instead)
3. **Permission Denied**: Gmail App Passwords should resolve most authentication issues

### Getting Help

- Test with dry run mode first: `python demo_analysis.py`
- Verify CSV file format matches expected columns (Name, Email, Total Score, Max Points)
- Check Gmail App Password setup at: https://myaccount.google.com/security

## License

This project is for educational use. Please ensure compliance with your institution's policies regarding student data and email communications.
