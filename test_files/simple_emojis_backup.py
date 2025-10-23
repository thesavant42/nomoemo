# Test File 1: Simple Emojis
# This file contains various simple emoji characters for testing

def print_status():
    print("Status: Good 👍")  # Simple smiley - should be detected
    print("Warning: Check this ⚠️")  # Warning sign - should be detected
    return True

# Function with emoji in comment
def calculate_sum(a, b):  # Adding numbers together
    result = a + b
    print("Result calculated successfully ✅")  # Checkmark - should be detected
    return result

# String literals with emojis
message = "Hello 🌍"  # Globe emoji in string
error_msg = "Something went wrong 😞"  # Sad face in string

# Code that looks like it might have emojis but doesn't
def safe_function():
    # This function has no emoji characters
    x = 1 + 1
    y = x * 2
    return y