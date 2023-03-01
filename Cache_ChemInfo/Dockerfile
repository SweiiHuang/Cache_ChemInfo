# Use an official Python runtime as the base image
FROM python:3


# Set the working directory in the container
WORKDIR /app


# Copy the file into the container
COPY . .
# Install the project dependencies

RUN pip install --upgrade pip --no-cache-dir

RUN pip install -r /app/requirements.txt --no-cache-dir

# Start the Django development server
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]

