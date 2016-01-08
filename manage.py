#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superstore.settings")

    from django.core.management import execute_from_command_line
    
    # For Cloud9 switch syncdb to migrate
    if sys.argv[-1] == 'syncdb':
        sys.argv[-1] = 'migrate'

    execute_from_command_line(sys.argv)
