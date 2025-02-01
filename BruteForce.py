import time
import itertools
import string
from multiprocessing import Pool, cpu_count

# Function that attempts to guess the password for a given length using parallelization
def attempt_password(args):
    target_password, characters, length = args
    counter = 0
    for guess in itertools.product(characters, repeat=length):
        counter += 1 
        if counter % 1000 == 0:  # Use a counter to track guesses
             print(''.join(guess))

        if ''.join(guess) == target_password:
            return ''.join(guess)
    return None

# Brute force function with parallelization and optimized settings
def brute_force_parallel(target_password, max_length):
    characters = string.ascii_lowercase  # Only lowercase letters (26 characters)
    num_cores = cpu_count()  # Get the number of CPU cores available
    start_time = time.time()

    # Parallelize the brute force process by splitting the work among available cores
    with Pool(processes=num_cores) as pool:
        for length in range(1, max_length + 1):  # Iterate over password lengths up to max_length
            tasks = [(target_password, characters, length)] * num_cores  # Distribute tasks
            results = pool.map(attempt_password, tasks)  # Run the brute force process
            for result in results:
                if result:
                    end_time = time.time()
                    return result, end_time - start_time  # Return the found password and time taken

    return None, None  # Return None if password wasn't found

if __name__ == "__main__":
    # Ask the user for the target password
    target_password = input("Enter the password to brute force: ")
    max_length = len(target_password)  # Set max_length based on the length of the target password
    print(f"Brute forcing password of length {max_length} using {cpu_count()} CPU cores...")

    # Call the brute force function
    result = brute_force_parallel(target_password, max_length=max_length)

    if result[0]:
        found_password, time_taken = result
        print(f"Password found: {found_password}")
        print(f"Time taken: {time_taken:.2f} seconds")
    else:
        print("Password not found.")
