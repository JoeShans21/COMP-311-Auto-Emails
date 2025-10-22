#!/usr/bin/env python3
"""
Demo script to run the Gradescope analysis without sending emails.
This is a safe way to test the analysis functionality.
"""

from gradescope_analyzer import GradescopeAnalyzer
import json


def main():
    print("Gradescope Analysis Demo")
    print("=" * 30)

    try:
        # Initialize analyzer
        analyzer = GradescopeAnalyzer("three-scores.csv", "two-scores.csv")

        # Run analysis
        print("Analyzing student performance...")
        categories = analyzer.analyze_student_performance()

        # Display results
        print("\nAnalysis Results:")
        print("-" * 20)

        total_students = sum(len(students) for students in categories.values())
        print(f"Total students analyzed: {total_students}")
        print()

        for category, students in categories.items():
            if students:
                print(f"{category.upper()} ({len(students)} students):")
                for student in students[:3]:  # Show first 3 students
                    print(
                        f"  • {student['name']} - Quiz 2: {student['quiz2_percentage']:.1f}%, Quiz 3: {student['quiz3_percentage']:.1f}%"
                    )
                if len(students) > 3:
                    print(f"  ... and {len(students) - 3} more")
                print()

        # Generate full report
        report = analyzer.generate_analysis_report()
        print(report)

        # Save analysis
        filename = analyzer.save_analysis()
        print(f"\nDetailed analysis saved to: {filename}")

        # Show email preview
        print("\n" + "=" * 50)
        print("EMAIL PREVIEW (DRY RUN)")
        print("=" * 50)

        results = analyzer.send_emails("", 0, "", "", dry_run=True)
        print(f"\nWould send {len(results['sent'])} emails total")

    except FileNotFoundError as e:
        print(f"Error: Could not find required CSV files. {e}")
        print(
            "Make sure 'three-scores.csv' and 'two-scores.csv' are in the current directory."
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
