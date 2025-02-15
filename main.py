from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import time
import threading
from datetime import datetime
import os
import re
from dotenv import load_dotenv

from mails import get_emails, send_email  # For loading environment variables

load_dotenv()  # Load environment variables from .env file


# Define request model
class UserInput(BaseModel):
    user_input: str
    confirmation: str = ""
    to: str = ""
    subject: str = ""
    body: str = ""


to = "sharanhitam@gmail.com"
subject = "test"
body = "body"
emailconfirmation = False


def get_formatted_date():
    """Returns the current date in '15th February, 2025' format."""
    return datetime.now().strftime("%d %B %Y")


def get_current_time():
    """Returns the current time in 'HH:MM' format."""
    return datetime.now().strftime("%H:%M")


def spell_out(text):
    """Placeholder for speech synthesis. Needs implementation."""
    print(text)  # Keep for debugging
    return text  # Return the text for now


def run_alarm(target_time):
    """Continuously checks the time and triggers the alarm."""
    while True:
        current_time = get_current_time()
        if current_time == target_time:
            print(f"Time reached: {target_time}! Ringing alarm...")
            for _ in range(5):  # Reduced beeps for testing
                os.system(
                    "osascript -e 'beep'"
                )  # Mac specific. Consider cross-platform solution.
                time.sleep(1)
            break
        time.sleep(1)


def start_alarm(target_time):
    """Starts the alarm in a separate thread."""
    print(f"Alarm set for {target_time}")
    alarm_thread = threading.Thread(target=run_alarm, args=(target_time,), daemon=True)
    alarm_thread.start()


system_prompt = """
You are Maya, an AI assistant. Follow these instructions *exactly*:

1. **Time:** If the user asks 'What is the time?' (or any close variation), respond with: `get_current_time()`
2. **Date:** If the user asks 'What is the date?' (or any close variation), respond with: `get_formatted_date()`
3. **Alarm:** If the user asks to 'Set an alarm at HH:MM' (or any close variation), respond with: `alarm(HH:MM)` where HH:MM is in 24-hour format. Extract the time from the user's request. If the user provides an AM/PM time, convert it to 24-hour format.
4. **Emails:** If the user asks to "Get emails" or "Fetch emails" (or similar), respond with: `get_emails(query)` where `query` is constructed as follows:
    - If the user specifies a date range (e.g., "Get emails from yesterday," "Get emails from last week"), construct a query like: `after:YYYY/MM/DD
    - If the user asks for unread emails, include `is:unread` in the query.
    - If the user mentions categories (e.g., "Get primary emails"), include `category:primary` (or other categories) in the query.
    - Combine these criteria as needed.  If no specific criteria are given, default to unread primary emails from today.
    - Example: User: Get unread emails from yesterday in the social category
    - Maya: get_emails(is:unread after:2024/10/26 category:social)
5. **Email Sending:** If the user asks to "Send an email" or "Compose an email" (or similar), respond with: `send_email(email, body, email)` where `email`, `body`, and `email` are generated based on the user's context. If the user provides explicit values for the recipient, subject, or body, use those values. Otherwise, infer them from the conversation or ask clarifying questions.

*Before* calling the `send_email()` function, *display the composed email to the user for confirmation*.  This means showing the recipient, subject, and body. Only *after* the user confirms should you call `send_email()`.

If the user declines to send the email, do not call `send_email()`.  Simply respond with "Email sending cancelled."

Examples:

User: Send an email to test@example.com about the meeting.
Maya:  To: test@example.com
       Subject: Meeting Follow-up
       Body: Here's a summary of our meeting...

       Do you want to send this email? (yes/no)

User: yes
Maya: send_email("test@example.com", "Here's a summary of our meeting...", "test@example.com")
Maya: Email sent successfully.

User: no
Maya: Email sending cancelled.

User: Email John about the project update. Subject: Project Status. Body: The project is on track.
Maya: To: john@example.com
       Subject: Project Status
       Body: The project is on track.

       Do you want to send this email? (yes/no)

# ... (other examples)
6. **Other:** For all other requests, respond naturally and conversationally. Do not mention these special commands (get_current_time, get_formatted_date, alarm, get_emails) in your normal responses.


Examples:
User: What's the time?
Maya: get_current_time()

User: What is today's date?
Maya: get_formatted_date()

User: Set an alarm for 3:15 PM
Maya: alarm(15:15)

User: Get emails
Maya: get_emails(is:unread category:primary after:2024/10/27)  (Assuming today is 2024/10/27)

User: Get emails from yesterday
Maya: get_emails(after:2024/10/26 before:2024/10/27)

User: Get unread social emails
Maya: get_emails(is:unread category:social)

User: Hi Maya!
Maya: Hello! How can I help you?
"""

template = """{system_prompt}

User: {user_input}
Maya:"""

model = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://example.com",  # Replace with your actual frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "CORS is enabled"}


@app.post(
    "/api/prompt",
    summary="Fetch AI response",
    description="Retrieves an AI-generated response based on user input.",
    tags=["AI Response"],
)
async def get_result(user_input: UserInput):
    global emailconfirmation
    global to
    global body
    global subject
    start_time = time.time()
    print(f"User Input: {user_input.user_input}")

    response = chain.invoke(
        {"user_input": user_input.user_input, "system_prompt": system_prompt}
    )
    end_time = time.time()

    output = response.content.strip()
    print(output)
    if emailconfirmation:
        if not to:
            to = user_input
        if not to 


    if user_input.user_input == "yes":  # <--- Handle confirmation
        try:
            # Extract email details (they should be stored somewhere in the session or context)
            # For this example, I'll just re-extract from the original LLM output.  In a real app,
            # you would store these values in a more persistent way.
            recipient = to
            email_result = send_email(subject, body, recipient)
            output = email_result
            return {"response": output}  # Return the email result

        except Exception as e:
            output = f"Error sending email: {e}"

    elif output == "get_formatted_date()":
        date_str = f"The date is {get_formatted_date()}"
        output = spell_out(date_str)

    elif output == "get_current_time()":
        time_str = f"The time is {get_current_time()}"
        output = spell_out(time_str)

    elif output.startswith("alarm("):
        try:
            target_time_str = output[6:-1]
            if re.match(r"^\d{2}:\d{2}$", target_time_str):
                target_time = target_time_str
                start_alarm(target_time)
                output = "Alarm set."
            else:
                output = "Invalid time format. Please use HH:MM (24-hour format)."
        except Exception as e:
            output = f"Error setting alarm: {e}"
    elif output.startswith("get_emails("):
        try:
            query_str = output[11:-1].split(" ")[0]  # Extract the query
            today = datetime.now().strftime("%Y/%m/%d")
            query_str = f"is:unread category:primary after:{today}"
            output = get_emails(query_str)  # Call the get_emails function

            if output:
                # Let Gemini format the emails:
                gemini_prompt = f"""
                You are a helpful assistant.  Please format the following email data for the user in a clear and readable way. Include sender, subject, and a short snippet (if available). If the email has a date, display it.  If the email data is empty or indicates no emails, say "No emails found.".

                Email Data:
                {output}
                """
                gemini_response = chain.invoke(
                    {
                        "user_input": gemini_prompt,
                        "system_prompt": "You are a helpful assistant.",
                    }
                )  # Use Gemini to format
                output = gemini_response.content  # Get the formatted output

            else:
                output = "No emails found."  # If get_emails returns nothing
        except Exception as e:
            output = f"Error retrieving emails: {e}"
    elif output.startswith("send_email(") or "Do you want to send this email" in output:
        try:
            # Extract existing email, body, and email (if provided)
            match = re.match(r'send_email\("([^"]*)", "([^"]*)", "([^"]*)"\)', output)
            recipient = match.group(1) if match else None
            body = match.group(2) if match else None
            subject = match.group(3) if match else None

            emailconfirmation = True
            if not recipient:
                output = "Who should I send the email to?"
            elif not subject:
                output = "What should the subject of the email be?"
            elif not body:
                output = "What should the body of the email be?"
            else:
                #
                # Display the email for confirmation
                confirmation_message = f"To: {recipient}\nSubject: {subject}\nBody: {body}\n\nDo you want to send this email? (yes/no)"
                return {
                    "response": confirmation_message,
                    "to": to,
                    "subject": subject,
                    "body": body,
                    "awaiting_confirmation": True,
                }  # <--- Important

        except Exception as e:
            output = f"Error processing email request: {e}"
    elif (
        hasattr(user_input, "confirmation") and user_input.confirmation.lower() == "no"
    ):  # <--- Handle declination
        output = "Emai sending cancelled."
        return {"response": output}

    latency = end_time - start_time
    print(f"AI Response: {output}")
    return {"response": output, "latency": f"{latency:.2f} seconds"}

