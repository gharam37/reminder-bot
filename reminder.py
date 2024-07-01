from flask import Flask , render_template, request
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
import datetime
import time

load_dotenv()

app = Flask(__name__)

# Google Sheets and Slack credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_SHEET_CREDENTIALS"), scope)
slack_token = os.getenv("SLACK_API_TOKEN")
slack_client = WebClient(token=slack_token)

def send_message(channel, text):
    slack_client.chat_postMessage(channel=channel, text=text)

def send_leave_message(name, email, comments, start_date, end_date, timestamp):
    message = f"{name} is taking leave from {start_date} to {end_date} 🏖️🎉"
    return message

def combine_leave_message(channel , messages):
    start = "Hey Zammit Techies! Reminding You that:"
    combined_message = "\n".join(messages)
    combined_message = f"{start}\n{combined_message}"
    print(combined_message)
    send_message(channel, combined_message)
    return combined_message
    
def parse_date(timestamp_str):
    # Example timestamp_str: '6/13/2024 15:03:27'
    return datetime.datetime.strptime(timestamp_str, '%m/%d/%Y').date()

def process_google_sheet():
    print("Processing Google Sheet data... From Server")
    client = gspread.authorize(creds)
    sheet = client.open("Zammit Tech PTO & Sick Leave Request (Responses)").sheet1

    
    # Fetch data from the sheet
    data = sheet.get_all_records()

    today = datetime.date.today()
    filtered_records = [record for record in data if parse_date(record['Start Date']) >= today]

    print(filtered_records)
    messages = []
    for row in filtered_records:

        name = row['Name']
        timestamp = row['Timestamp']
        email = row['Email Address']
        comments = row['Comments']
        start_date = row['Start Date']
        end_date = row['End Date']
        message = send_leave_message(name, email, comments, start_date, end_date, timestamp)
        messages.append(message)
    combine_leave_message('test-zimo' ,messages)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-notification', methods=['POST'])
def send_notification():
    print("Clicked send notification")
    try:
        return process_google_sheet()
    except Exception as e:
        return f'Error sending notification: {e}'
    
def execute_periodically():
    while True:
        try:
            # Process Google Sheet data
            process_google_sheet()
            print("Processed Google Sheet data.")

            # Sleep for 10 minutes
            time.sleep(600)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)  # Sleep longer on error to avoid rapid retries

if __name__ == '__main__':
    execute_periodically()
    # Uncomment the line below if you want to run the Flask app concurrently
    # app.run(debug=False)
