import os
import time
import random
import json
from datetime import datetime
import threading

# Configuration
LOG_DIR = './shared/logs'  # Directory where logs will be generated
LOG_FILES = ['backend.log', 'frontend.log', 'database.log', 'backend2.log']
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
MESSAGES = {
    'backend': [
        'User authentication succeeded.',
        'Database connection established.',
        'Cache miss for key user_123.',
        'Failed to retrieve data from API.',
        'Scheduled task completed successfully.',
        'Unexpected error occurred in processing request.'
    ],
    'frontend': [
        'User clicked the login button.',
        'Page loaded successfully.',
        'JavaScript error on line 45.',
        'User session expired.',
        'Resource loaded: main.css.',
        'UI component rendered.'
    ],
    'database': [
        'Query executed in 120ms.',
        'Database connection lost.',
        'Data backup completed.',
        'Failed to write to table orders.',
        'Index rebuilt successfully.',
        'Replication lag detected.'
    ],
    'backend2': [  # Messages specific to backend2
        'Processed transaction ID 78910.',
        'User profile updated successfully.',
        'Cache cleared for session ID abc123.',
        'Failed to send notification email.',
        'New API endpoint deployed.',
        'Scheduled maintenance task initiated.'
    ]
}
SLEEP_INTERVAL = (1, 5)  # Range in seconds between log entries per component

def ensure_log_directory_exists(directory):
    """
    Ensures that the specified log directory exists.
    If it does not exist, the directory is created.
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Created log directory at: {directory}")
        except OSError as e:
            print(f"Failed to create log directory {directory}: {e}")
            exit(1)

def generate_log_entry(component):
    """
    Generates a single log entry for the specified component.
    Plain-text format for backend, frontend, database.
    JSON format for backend2.
    """
    timestamp = datetime.now().isoformat()
    level = random.choice(LOG_LEVELS)
    message = random.choice(MESSAGES[component])

    if component == 'backend2':
        # Generate a JSON log entry
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "component": component,
            "message": message,
            "transaction_id": random.randint(10000, 99999),  # Example additional field
            "user_id": random.randint(1000, 9999)  # Example additional field
        }
        # Convert the dictionary to a JSON-formatted string
        log_entry_str = json.dumps(log_entry)
    else:
        # Generate a plain-text log entry
        log_entry_str = f"{timestamp}  level={level} component={component} {message}"

    return log_entry_str

def write_log_entry(log_file, log_entry):
    """
    Appends the generated log entry to the specified log file.
    Also prints the log entry to the console for real-time monitoring.
    """
    try:
        with open(log_file, 'a') as f:
            f.write(log_entry + '\n')
        print(log_entry)  # Optional: Print to console
    except IOError as e:
        print(f"Failed to write to log file {log_file}: {e}")

def log_generator(component, log_file):
    """
    Continuously generates and writes log entries for a specific component.
    """
    print(f"Starting log generation for '{component}'. Writing to '{log_file}'")
    try:
        while True:
            log_entry = generate_log_entry(component)
            write_log_entry(log_file, log_entry)
            sleep_time = random.uniform(*SLEEP_INTERVAL)
            time.sleep(sleep_time)
    except KeyboardInterrupt:
        print(f"\nLog generation for '{component}' stopped by user.")

def main():
    """
    Main function to initiate log generation for all configured components.
    """
    # Ensure the log directory exists
    ensure_log_directory_exists(LOG_DIR)
    
    threads = []
    for log_file in LOG_FILES:
        component = log_file.split('.')[0]  # Assuming filename format 'component.log'
        full_log_path = os.path.join(LOG_DIR, log_file)
        thread = threading.Thread(target=log_generator, args=(component, full_log_path), daemon=True)
        thread.start()
        threads.append(thread)
    
    print("Log generation is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nAll log generation threads stopped by user.")

if __name__ == "__main__":
    main()
