# Use an official Python runtime as a parent image
FROM python:3.8.2-alpine

# Set the working directory
WORKDIR /app

# Install Git
RUN apk update && apk add --no-cache git

# Copy the dependencies file to the working directory
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
EXPOSE 5000

# Set the command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
