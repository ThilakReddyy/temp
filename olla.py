import ollama
from datetime import datetime
import os
import time
import threading


def get_current_time():
    return datetime.now().strftime("%H:%M")


def alarm(target_time):
    def run_alarm():
        while True:
            current_time = get_current_time()
            print(current_time, target_time)
            if current_time == target_time:
                print(f"Time reached: {target_time}! Ringing alarm...")
                for _ in range(10):  # Beep 10 times
                    os.system("osascript -e 'beep'")
                    time.sleep(1)
                break
            time.sleep(1)

    # Run alarm in a separate thread
    alarm_thread = threading.Thread(target=run_alarm, daemon=True)
    alarm_thread.start()


system_prompt = """
You are a general assistant. If the user asks 'What is the time?', only respond with get_current_time().
If the user asks to 'Set an alarm at HH:MM' or 'wake me up at HH:MM', respond with alarm(target_time).
Do not provide any additional text or explanations. If it does not follow the above conditions respond with normal output
Example:
User: set an alarm at 03:15 pm
Assistant: alarm(15:15)
"""

msgs = []
while True:
    user_input = input("Enter command: ").strip()

    response = ollama.chat(
        model="llama3.1",
        messages=msgs,
    )

    output = response["message"]["content"].strip()
    print(output)

    if output == "get_current_time()":
        print(get_current_time())
    elif output.startswith("alarm("):
        target_time = output.replace("alarm(", "").replace(")", "").strip()
        print(f"Alarm set for {target_time}")

        # Start the alarm in a separate thread
        alarm(target_time)

    elif user_input.lower() == "exit":
        break
    else:
        print(output)
    msgs.append({"User": user_input, "Assistant": output})
