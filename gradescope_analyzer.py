#!/usr/bin/env python3
"""
Gradescope Analysis and Email System (Gmail Version)
Analyzes student performance and sends encouraging emails via Gmail based on performance trends.
"""

import pandas as pd
import numpy as np
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Tuple
import json
from datetime import datetime
import os


class GradescopeAnalyzer:
    def __init__(self, three_scores_file: str, two_scores_file: str):
        """Initialize the analyzer with CSV files."""
        self.three_scores = pd.read_csv(three_scores_file)
        self.two_scores = pd.read_csv(two_scores_file)
        self.student_analysis = {}

    def clean_data(self):
        """Clean and prepare the data for analysis."""
        # Remove rows with missing names or emails
        self.three_scores = self.three_scores.dropna(subset=["Name", "Email"])
        self.two_scores = self.two_scores.dropna(subset=["Name", "Email"])

        # Convert scores to numeric, handling any non-numeric values
        self.three_scores["Total Score"] = pd.to_numeric(
            self.three_scores["Total Score"], errors="coerce"
        )
        self.two_scores["Total Score"] = pd.to_numeric(
            self.two_scores["Total Score"], errors="coerce"
        )

        # Calculate percentages
        self.three_scores["Percentage"] = (
            self.three_scores["Total Score"] / self.three_scores["Max Points"]
        ) * 100
        self.two_scores["Percentage"] = (
            self.two_scores["Total Score"] / self.two_scores["Max Points"]
        ) * 100

    def analyze_student_performance(self):
        """Analyze individual student performance and categorize them."""
        self.clean_data()

        # Merge the two datasets on Name and Email
        merged_data = pd.merge(
            self.three_scores[["Name", "Email", "Total Score", "Percentage"]].rename(
                columns={"Total Score": "Quiz3_Score", "Percentage": "Quiz3_Percentage"}
            ),
            self.two_scores[["Name", "Email", "Total Score", "Percentage"]].rename(
                columns={"Total Score": "Quiz2_Score", "Percentage": "Quiz2_Percentage"}
            ),
            on=["Name", "Email"],
            how="outer",
        )

        # Fill missing values with 0 for students who didn't take a quiz
        merged_data = merged_data.fillna(0)

        # Categorize students
        categories = {
            "excelling": [],  # High scores on both quizzes
            "improving": [],  # Low on quiz 2, high on quiz 3
            "struggling": [],  # Low scores on both quizzes
            "declining": [],  # High on quiz 2, low on quiz 3
            "consistent": [],  # Similar performance on both quizzes
        }

        for _, student in merged_data.iterrows():
            name = student["Name"]
            email = student["Email"]
            quiz2_pct = student["Quiz2_Percentage"]
            quiz3_pct = student["Quiz3_Percentage"]

            # Skip students with no valid scores
            if quiz2_pct == 0 and quiz3_pct == 0:
                continue

            student_data = {
                "name": name,
                "email": email,
                "quiz2_score": student["Quiz2_Score"],
                "quiz2_percentage": quiz2_pct,
                "quiz3_score": student["Quiz3_Score"],
                "quiz3_percentage": quiz3_pct,
                "improvement": quiz3_pct - quiz2_pct if quiz2_pct > 0 else 0,
            }

            # Categorize based on performance patterns
            # Calculate improvement for better categorization
            improvement = quiz3_pct - quiz2_pct if quiz2_pct > 0 else quiz3_pct

            if quiz2_pct >= 85 and quiz3_pct >= 85:
                categories["excelling"].append(student_data)
            elif improvement >= 15 or (quiz2_pct < 70 and quiz3_pct >= 75):
                # Significant improvement: 15+ point improvement OR low quiz2 but good quiz3
                categories["improving"].append(student_data)
            elif quiz2_pct < 60 and quiz3_pct < 60:
                # Both scores are low
                categories["struggling"].append(student_data)
            elif quiz2_pct >= 75 and quiz3_pct < 60:
                # High quiz2 but low quiz3
                categories["declining"].append(student_data)
            else:
                # Similar performance or moderate changes
                categories["consistent"].append(student_data)

        self.student_analysis = categories
        return categories

    def generate_analysis_report(self) -> str:
        """Generate a comprehensive analysis report."""
        if not self.student_analysis:
            self.analyze_student_performance()

        report = []
        report.append("=" * 60)
        report.append("GRADESCOPE PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # Summary statistics
        total_students = sum(
            len(students) for students in self.student_analysis.values()
        )
        report.append(f"Total Students Analyzed: {total_students}")
        report.append("")

        # Category breakdown
        for category, students in self.student_analysis.items():
            if students:
                report.append(
                    f"{category.upper()} STUDENTS ({len(students)} students):"
                )
                report.append("-" * 40)

                for student in students:
                    report.append(f"• {student['name']} ({student['email']})")
                    if student["quiz2_percentage"] > 0:
                        report.append(f"  Quiz 2: {student['quiz2_percentage']:.1f}%")
                    if student["quiz3_percentage"] > 0:
                        report.append(f"  Quiz 3: {student['quiz3_percentage']:.1f}%")
                    if student["improvement"] != 0:
                        report.append(f"  Improvement: {student['improvement']:+.1f}%")
                    report.append("")

        return "\n".join(report)

    def get_email_templates(self) -> Dict[str, str]:
        """Get email templates for different student categories."""
        return {
            "excelling": """
Subject: Excellent Work in COMP 311! 🌟

Hi {name},

I hope this email finds you well! I wanted to take a moment to recognize your outstanding performance in COMP 311.

Your consistent high scores on both Quiz 2 ({quiz2_percentage:.1f}%) and Quiz 3 ({quiz3_percentage:.1f}%) demonstrate your strong understanding of the course material. Your dedication and hard work are truly commendable!

Keep up the excellent work, and don't hesitate to reach out if you have any questions or if you'd like to explore any topics in more depth.

Best regards,
Your COMP 311 Instructor
""",
            "improving": """
Subject: Great Improvement in COMP 311! 🎉

Hi {name},

I wanted to reach out and congratulate you on your significant improvement in COMP 311!

I noticed that while you scored {quiz2_percentage:.1f}% on Quiz 2, you've made an impressive jump to {quiz3_percentage:.1f}% on Quiz 3 - that's a {improvement:+.1f} percentage point improvement! This shows real dedication and growth.

Your hard work is paying off, and I'm excited to see this positive trajectory continue. Keep up the great work!

If you have any questions or need additional support, please don't hesitate to reach out.

Best regards,
Your COMP 311 Instructor
""",
            "struggling": """
Subject: Let's Work Together to Succeed in COMP 311 💪

Hi {name},

I hope you're doing well. I wanted to reach out because I noticed you might be having some challenges with the course material.

Your current scores (Quiz 2: {quiz2_percentage:.1f}%, Quiz 3: {quiz3_percentage:.1f}%) suggest there might be some concepts that need additional attention. Remember, it's completely normal to face challenges in computer science courses, and the important thing is how we address them.

I'd like to offer some support:
- Office hours are available for one-on-one help
- Study groups can be incredibly beneficial
- I'm here to answer any questions you might have

Let's work together to get you back on track. What specific topics would you like to focus on?

Best regards,
Your COMP 311 Instructor
""",
            "declining": """
Subject: Let's Get Back on Track in COMP 311 📈

Hi {name},

I hope you're doing well. I wanted to reach out because I noticed a concerning trend in your recent quiz performance.

While you did well on Quiz 2 ({quiz2_percentage:.1f}%), your Quiz 3 score ({quiz3_percentage:.1f}%) suggests there might be some challenges with the newer material.

This could be due to various factors - perhaps the concepts are getting more complex, or there might be external factors affecting your studies. Whatever the case, I'm here to help.

I'd encourage you to:
- Review the Quiz 3 material more thoroughly
- Attend office hours for clarification
- Consider forming a study group
- Reach out to me with any specific questions

Let's work together to get you back on the right track. What can I do to support you?

Best regards,
Your COMP 311 Instructor
""",
            "consistent": """
Subject: Steady Progress in COMP 311! 👍

Hi {name},

I hope this email finds you well! I wanted to take a moment to acknowledge your consistent performance in COMP 311.

Your scores show steady progress (Quiz 2: {quiz2_percentage:.1f}%, Quiz 3: {quiz3_percentage:.1f}%), which indicates a solid understanding of the course material. Consistency is a valuable trait in computer science, and you're demonstrating it well.

Keep up the good work, and remember that I'm here if you have any questions or want to explore any topics further.

Best regards,
Your COMP 311 Instructor
""",
        }

    def send_emails(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str,
        dry_run: bool = True,
    ) -> Dict[str, List[str]]:
        """Send emails to students based on their performance category."""
        if not self.student_analysis:
            self.analyze_student_performance()

        templates = self.get_email_templates()
        results = {"sent": [], "failed": [], "skipped": []}

        if dry_run:
            print("DRY RUN MODE - No emails will actually be sent")
            print("=" * 50)

        for category, students in self.student_analysis.items():
            if not students:
                continue

            print(f"\nProcessing {category} students...")

            for student in students:
                try:
                    # Format the email template
                    email_content = templates[category].format(
                        name=student["name"],
                        quiz2_percentage=student["quiz2_percentage"],
                        quiz3_percentage=student["quiz3_percentage"],
                        improvement=student["improvement"],
                    )

                    if dry_run:
                        print(f"Would send to {student['name']} ({student['email']})")
                        print(
                            f"Subject: {email_content.split('Subject: ')[1].split('\\n')[0]}"
                        )
                        print("-" * 30)
                        results["sent"].append(
                            f"{student['name']} ({student['email']}) - DRY RUN"
                        )
                    else:
                        # Actually send the email
                        self._send_single_email(
                            smtp_server,
                            smtp_port,
                            sender_email,
                            sender_password,
                            student["email"],
                            email_content,
                        )
                        results["sent"].append(
                            f"{student['name']} ({student['email']})"
                        )

                except Exception as e:
                    error_msg = (
                        f"{student['name']} ({student['email']}) - Error: {str(e)}"
                    )
                    results["failed"].append(error_msg)
                    print(f"Failed to send email to {student['name']}: {str(e)}")

        return results

    def _send_single_email(
        self,
        smtp_server: str,
        smtp_port: int,
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        email_content: str,
    ):
        """Send a single email."""
        # Parse subject and body
        lines = email_content.strip().split("\n")
        subject = lines[0].replace("Subject: ", "")
        body = "\n".join(lines[1:]).strip()

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

    def save_analysis(self, filename: str = None):
        """Save the analysis results to a JSON file."""
        if not self.student_analysis:
            self.analyze_student_performance()

        if filename is None:
            filename = (
                f"gradescope_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

        with open(filename, "w") as f:
            json.dump(self.student_analysis, f, indent=2)

        print(f"Analysis saved to {filename}")
        return filename


def main():
    """Main function to run the analysis with Gmail."""
    print("Gradescope Analysis and Email System (Gmail Version)")
    print("=" * 55)

    # Initialize analyzer
    analyzer = GradescopeAnalyzer("three-scores.csv", "two-scores.csv")

    # Analyze student performance
    print("Analyzing student performance...")
    categories = analyzer.analyze_student_performance()

    # Generate and display report
    report = analyzer.generate_analysis_report()
    print("\n" + report)

    # Save analysis
    analyzer.save_analysis()

    # Ask about sending emails
    print("\n" + "=" * 60)
    print("EMAIL SENDING OPTIONS")
    print("=" * 60)
    print("1. Dry run (preview emails without sending)")
    print("2. Send emails using Gmail")
    print("3. Skip email sending")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        print("\nRunning dry run...")
        results = analyzer.send_emails("", 0, "", "", dry_run=True)
        print(f"\nDry run complete. Would have sent {len(results['sent'])} emails.")

    elif choice == "2":
        print("\nGmail configuration:")
        print("Make sure you have:")
        print("1. Enabled 2-Factor Authentication on Gmail")
        print("2. Generated an App Password")
        print("3. Go to: https://myaccount.google.com/security")
        print("4. Click '2-Step Verification' → 'App passwords'")
        print("5. Generate password for 'Mail'")
        print()

        sender_email = input("Your Gmail address: ").strip()
        app_password = input("Gmail app password: ").strip()

        if not sender_email or not app_password:
            print("❌ Gmail address and app password are required.")
            return

        # Gmail SMTP settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        confirm = (
            input(
                f"\nSend emails to {sum(len(students) for students in categories.values())} students using Gmail? (y/N): "
            )
            .strip()
            .lower()
        )
        if confirm == "y":
            print("\nSending emails via Gmail...")
            results = analyzer.send_emails(
                smtp_server, smtp_port, sender_email, app_password, dry_run=False
            )
            print(f"\nEmail sending complete!")
            print(f"Sent: {len(results['sent'])}")
            print(f"Failed: {len(results['failed'])}")

            if results["failed"]:
                print("\nFailed emails:")
                for failure in results["failed"]:
                    print(f"  - {failure}")
        else:
            print("Email sending cancelled.")

    else:
        print("Skipping email sending.")


if __name__ == "__main__":
    main()
