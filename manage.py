#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

def main():
    load_dotenv()  # Correct method call
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoauthapi1.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        print("Error importing Django:", exc)
        print("PYTHONPATH:", sys.path)
        print("Are you sure Django is installed and your virtual environment is activated?")
        sys.exit(1)  # Exit with a non-zero status to indicate failure
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
