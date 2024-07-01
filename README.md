## Installation

1- Create a GCP project and a service account to it
2- Add service_account.json to your root directory
3- enable Google Sheets API and Google Drive API in your GCP product

## How to run

```
docker build -t reminder-bot .

docker run -it -p 5000:5000 -e "SLACK_API_TOKEN=<Your slack bot token>" reminder-bot

```
