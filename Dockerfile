# Use the official Python image as the base image
FROM python:3.11.3-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the application dependencies
RUN apt-get update && apt-get install -y libgeos-c1v5 && rm -rf /var/lib/apt/lists/*

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Copy the application code to the working directory
COPY . .

# Start the application with Gunicorn
CMD ["python3", "app.py"]
