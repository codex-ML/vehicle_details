# Use an official Python runtime as a parent image
worker: python main.py

FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script into the container at /usr/src/app/
COPY main.py .

# Install any necessary dependencies
RUN pip install telebot requests

# Run your script when the container launches
CMD ["python", "main.py"]
