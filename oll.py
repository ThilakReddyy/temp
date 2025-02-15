import ollama
import os
import time
import threading
from datetime import datetime


def get_formatted_date():
    """Returns the current date in '15th February, 2025' format."""
    return datetime.now().strftime("%d %B %Y")


def get_current_time():
    """Returns the current time in 'HH:MM' format."""
    print(datetime.now().strftime("%H:%M"))
    return str(datetime.now())


def spell_out(text):
    """Use Ollama to convert text into a natural spoken format."""
    print(text)
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "system",
                "content": "Convert the given input into a english format without adding explanations. ",
            },
            {"role": "user", "content": f"convert this {text}"},
        ],
    )
    return response["message"]["content"].strip()


def run_alarm(target_time):
    """Continuously checks the time and triggers the alarm at the specified target time."""
    while True:
        current_time = get_current_time()
        if current_time == target_time:
            print(f"Time reached: {target_time}! Ringing alarm...")
            for _ in range(30):  # Beep 10 times
                os.system("osascript -e 'beep'")
                time.sleep(1)
            break
        time.sleep(1)


def start_alarm(target_time):
    """Runs the alarm in a separate thread to keep the main program responsive."""
    print(f"Alarm set for {target_time}")
    alarm_thread = threading.Thread(target=run_alarm, args=(target_time,), daemon=True)
    alarm_thread.start()


system_prompt = """
You are an assistant. You name is Maya and also i can call you as assistant
- If the user asks 'What is the time?', only respond with get_current_time().
- If the user asks 'What is the date?', only respond with get_formatted_date().
- If the user asks to 'Set an alarm at HH:MM', respond with alarm(target_time).
 If it does not follow the above conditions respond with normal output
Example:
user: set an alarm at 03:15 pm
assistant: alarm(15:15)
user: wake me up at 5:05 pm 
assistant: alarm(17:05)
user: hi
assistant: hello how can i help you?
"""

msgs = [{"role": "system", "content": system_prompt}]
while True:
    user_input = input("User: ").strip()

    msgs.append({"role": "user", "content": user_input})

    response = ollama.chat(
        model="llama3.1",
        messages=msgs,
    )

    output = response["message"]["content"].strip()

    if output == "get_formatted_date()":
        date_str = f"The date is {get_formatted_date()}"
        output = spell_out(date_str)

    elif "get_current_time()" in output:
        output = spell_out("what is the time?" + get_current_time())

    elif output.startswith("alarm("):
        target_time = output.replace("alarm(", "").replace(")", "").strip()
        start_alarm(target_time)  # Runs the alarm without blocking

    elif user_input.lower() == "exit":
        break
    msgs.append({"role": "assistant", "content": output})

    print(msgs)

