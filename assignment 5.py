# Program to validate PAN Number using Regular Expression

import re

pan = input("Enter PAN Number: ")

# Regular expression for standard PAN format
pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

# Check the PAN
if re.fullmatch(pattern, pan):
    print("Valid PAN Number")
else:
    print("Invalid PAN Number")