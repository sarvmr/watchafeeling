# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the API Gateway will listen on
EXPOSE 5002

# Define environment variables (if needed)


# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
