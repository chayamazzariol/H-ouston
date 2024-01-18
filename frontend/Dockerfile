# Use a Python base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files to the container
COPY ./app /app
COPY requirements.txt /app
RUN echo 'export PYTHONPATH="$PYTHONPATH:/app/app"' > /root/.bashrc

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask app will run
EXPOSE 80

# Command to run the application
#CMD ["python", "app/main.py"]

# Command to keep the container running
CMD ["tail", "-f", "/dev/null"]