# Use Python 3.10 slim-buster as the base image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Update package lists and install system dependencies
RUN apt-get update -y && \
    apt-get install -y \
    awscli \
    ffmpeg \
    libsm6 \
    libxext6 \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Set the default command to run the application with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]