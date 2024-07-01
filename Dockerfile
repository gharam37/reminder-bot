# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy the service account credentials into the container
COPY service_account.json /app/service_account.json

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=reminder.py
ENV GOOGLE_SHEET_CREDENTIALS=/app/service_account.json
ARG SLACK_API_TOKEN

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "reminder:app"]