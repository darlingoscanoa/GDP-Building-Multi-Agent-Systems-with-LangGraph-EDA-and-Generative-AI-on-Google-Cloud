# Python image to use.
FROM python:3.12.8-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

EXPOSE 8080

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]