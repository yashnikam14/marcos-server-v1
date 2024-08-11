import os
from pathlib import Path
from datetime import datetime

def log_message(message):
    filename = '{}-{}-{}-logfile.log'.format(datetime.now().strftime('%Y'), datetime.now().strftime('%m'), datetime.now().strftime('%d'))
    base_dir = Path.home() / 'users' / 'var'
    log_file_path = base_dir / filename

    # Ensure the directory exists
    base_dir.mkdir(parents=True, exist_ok=True)

    # Append message to the log file
    with open(log_file_path, 'a') as file:
        file.write("{}\n".format(message))

