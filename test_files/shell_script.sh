#!/bin/bash
# Test File 5: Binary-like Content
# This file is designed to test binary file detection

# This file should be processed as text but contains some unusual characters
echo "Processing data..."

# Some escape sequences that might confuse binary detection
echo -e "\x1b[32mGreen text\x1b[0m"
echo -e "\x1b[31mRed text\x1b[0m"

# But no actual emojis should be in this file
echo "Status: Complete"
echo "No emojis here!"

# Test with some special characters that are NOT emojis
echo "Copyright: (c) 2025"
echo "Trademark: (tm)"
echo "Registered: (r)"

exit 0