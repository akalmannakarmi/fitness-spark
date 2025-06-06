# Use the official Python image
FROM python:3.13.2-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the server
CMD ["python", "main.py"]
