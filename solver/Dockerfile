# Use an official Python runtime as a parent image
FROM python:3.11.7-slim-bookworm

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
#CMD ["python3", "solver.py"]
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]
#CMD ["python3", "api.py"]
