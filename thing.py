import math

# Dictionary of common passwords
common_passwords = ["password", "123456", "qwerty", "letmein", "password123"]

def calculate_entropy(password):
    pool_size = 0
    if any(char.islower() for char in password):
        pool_size += 26
    if any(char.isupper() for char in password):
        pool_size += 26
    if any(char.isdigit() for char in password):
        pool_size += 10
    if any(not char.isalnum() for char in password):
        pool_size += 32  # Approximation for special characters

    if pool_size == 0:  # Prevent math error for empty passwords
        return 0
    entropy = len(password) * math.log2(pool_size)
    return entropy

def score_password(password):
    # Entropy calculation
    entropy = calculate_entropy(password)
    if entropy < 28:  # Example thresholds based on entropy
        score = 2
    elif entropy < 35:
        score = 5
    else:
        score = 8

    # Check if the password is in a common list
    if password in common_passwords:
        score -= 3

    # Ensure score is between 1 and 10
    return max(1, min(10, score))

def suggest_improvements(password):
    suggestions = []
    if len(password) < 8:
        suggestions.append("Increase the password length to at least 8 characters.")
    if not any(char.isupper() for char in password):
        suggestions.append("Add at least one uppercase letter.")
    if not any(char.isdigit() for char in password):
        suggestions.append("Include at least one number.")
    if not any(not char.isalnum() for char in password):
        suggestions.append("Use at least one special character (e.g., @, #, $, etc.)")
    return suggestions

# Example usage
password = input("Enter your password: ")
score = score_password(password)

print(f"Password Score: {score}/10")


suggestions = suggest_improvements(password)
if suggestions:
    print("❌ Your password could be stronger. Suggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")
else:
    print("✅ Your password is strong!")
