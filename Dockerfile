# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Add a label to identify the project
LABEL project="queuetopia-account-mgr"

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 5005

# Command to run the application
CMD ["python", "app.py"]

