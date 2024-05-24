import gspread
from oauth2client.service_account import ServiceAccountCredentials

from slack_sdk import WebClient
import requests
import os
from dotenv import load_dotenv


load_dotenv()

# Create a google project and enable the google sheets API , google drive API
# Create a service account and download the json credentials
# Share the google sheet with the service account email
# Read the google sheet using the below code

def send_message(channel, text , client):
    client.chat_postMessage(channel=channel, text=text)


def send_leave_message(name, email, comments, leave_date):
    message = f"{name} will be on leave on the date of {leave_date}. Please contact them at {email} if you need anything. They also wanted to let you know that {comments}"
    return message
    

def main():
    print("Hello world")
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_SHEET_CREDENTIALS"), scope)

    print(scope)
    print(creds)
    client = gspread.authorize(creds)

    print(client)

    # # Open the Google Sheet
    sheet = client.open("test").sheet1
    print(sheet)

    # # Fetch data from the sheet
    data = sheet.get_all_records()

    

    print(data)
    slack_token = os.getenv("SLACK_TOKEN")
    slack_client = WebClient(token=slack_token)

    for row in data:
        print(row)
        name = row['Name']
        email = row['Email']
        comments = row['Comments']
        leave_date = row['Leave Date']
        message = send_leave_message(name, email, comments, leave_date)
        print(message)
        send_message("general", message, slack_client)



#     api_url = "https://slack.com/api/conversations.list"

# # Headers with authentication token
#     headers = {
#         "Authorization": f"Bearer {slack_token}",
#         "Content-Type": "application/json"
#     }

# # Make the API call
#     response = requests.get(api_url, headers=headers)
#     channels = response.json()['channels']
#     for channel in channels:
#         print(channel['name'])
    # send_message("general", "Never mind me I'm Playing", slack_client)






if __name__ == "__main__":
    main()