import time
import itertools
import string
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
from tabulate import tabulate

import itertools
import string
import time
from multiprocessing import Pool, cpu_count

# Brute Force Attack
def attempt_password(args):
    target_password, characters, length, max_duration, start_time = args
    for guess in itertools.product(characters, repeat=length):
        if time.time() - start_time > max_duration:  # Check if time exceeded
            return None
        if ''.join(guess) == target_password:
            return ''.join(guess)
    return None

def brute_force_parallel(target_password, max_length, max_duration=60):
    characters = string.ascii_lowercase + string.digits
    num_cores = cpu_count()
    start_time = time.time()

    with Pool(processes=num_cores) as pool:
        for length in range(1, max_length + 1):
            tasks = [(target_password, characters, length, max_duration, start_time)] * num_cores
            results = pool.map(attempt_password, tasks)
            for result in results:
                if result:
                    end_time = time.time()
                    return result, end_time - start_time

    return None, None

# Dictionary Attack
password_list = [
    "123456", "password", "123456789", "qwerty", "12345678", "abc123",
    "password1", "123123", "admin", "letmein", "welcome", "monkey",
    "football", "iloveyou", "sunshine", "1234", "princess", "dragon",
    "trustno1", "superman", "batman", "secure", "12345", "passw0rd",
    "shadow", "ashley", "michael", "charlie", "jordan", "buster",
    "soccer", "jennifer", "hunter", "maggie", "peanut", "ginger",
    "flower", "freedom", "robert", "taylor", "daniel", "cookie",
    "pepper", "hannah", "tigger", "volleyball", "snoopy", "bailey",
    "matthew", "harley", "summer", "dallas", "morgan", "amanda",
]

def dictionary_attack(target):
    start_time = time.time()
    for password in password_list:
        if password == target:
            end_time = time.time()
            return password, end_time - start_time
    return None, None

# Social Engineering Attack
personal_info = {
    "name": "JohnDoe",
    "birthday": "1990-03-15",
    "pet_name": "Fluffy",
    "favorite_color": "Blue"
}

def generate_social_passwords(info):
    patterns = [
        info['name'].lower(),
        info['birthday'].replace("-", ""),
        info['pet_name'].lower() + "123",
        info['favorite_color'].lower() + "2025",
        info['name'][:3].lower() + "@2021",
        info['pet_name'].lower() + "!",
    ]
    return patterns

def social_engineering_attack(target, info):
    passwords = generate_social_passwords(info)
    start_time = time.time()
    for password in passwords:
        if password == target:
            end_time = time.time()
            return password, end_time - start_time
    return None, None

# Visualization and Execution
if __name__ == "__main__":
    target_passwords = []  # Collect passwords from user input
    num_passwords = 3
    print(f"Enter {num_passwords} passwords to test:")
    for i in range(num_passwords):
        target_passwords.append(input(f"Password {i + 1}: "))

    all_results = {}

    for i, target_password in enumerate(target_passwords, 1):
        print(f"\nTesting Password {i}: {target_password}")
        results = {}
        
        print("\nRunning Brute Force Attack...")
        results['Brute Force'] = brute_force_parallel(target_password, max_length=len(target_password))
        
        print("\nRunning Dictionary Attack...")
        results['Dictionary'] = dictionary_attack(target_password)
        
        print("\nRunning Social Engineering Attack...")
        results['Social Engineering'] = social_engineering_attack(target_password, personal_info)
        
        all_results[target_password] = results  # Store results for each password

    # Aggregate results for visualization
    aggregated_times = {'Brute Force': 0, 'Dictionary': 0, 'Social Engineering': 0}
    aggregated_successes = {'Brute Force': 0, 'Dictionary': 0, 'Social Engineering': 0}

    for password, results in all_results.items():
        for method, (found, time_taken) in results.items():
            if found:
                aggregated_successes[method] += 1
                aggregated_times[method] += time_taken

    # Visualization: Bar and Pie Chart
    methods = list(aggregated_times.keys())
    total_times = [aggregated_times[method] for method in methods]
    success_counts = [aggregated_successes[method] for method in methods]

    # Bar Chart for Aggregated Time Taken
    plt.figure(figsize=(10, 6))
    plt.bar(methods, total_times, color=['blue', 'green', 'red'])
    plt.xlabel('Attack Methods')
    plt.ylabel('Total Time Taken (s)')
    plt.title('Total Time Taken for Each Attack Method Across All Passwords')
    plt.show()

    # Pie Chart for Aggregated Success Rates
    plt.figure(figsize=(8, 8))
    plt.pie(success_counts, labels=methods, autopct='%1.1f%%', startangle=140, colors=['blue', 'green', 'red'])
    plt.title('Success Rates of Attack Methods Across All Passwords')
    plt.show()

    # Tabulate Results for Each Password
    for password, results in all_results.items():
        print(f"\nResults for Password: {password}")
        table = [[method, results[method][0] if results[method][0] else "Not Found", 
                  f"{results[method][1]:.2f} seconds" if results[method][1] else "N/A"] for method in results]
        print(tabulate(table, headers=["Method", "Password Found", "Time Taken"], tablefmt="grid"))
