import os
import time
from datetime import datetime

# Set target time (24-hour format: HH:MM:SS)
target_time = "15:09"  # Change this to your desired time


def alarm(target_time):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        print(current_time, target_time)
        if current_time == target_time:
            print("Time reached! Ringing alarm...")
            for _ in range(10):  # Beep 10 times
                os.system("osascript -e 'beep'")
                time.sleep(1)  # Delay between beeps
            break  # Exit after ringing
        time.sleep(1)  # Check time every second


def get_current_time():
    return datetime.now().strftime("%H:%M")  # Returns time in HH:MM:SS format


# Example usage
print("Current time:", get_current_time())
