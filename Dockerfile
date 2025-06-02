# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy requirements.txt into the container at /app
COPY src/requirements.txt ./requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ← Add this line to pull in Plotly if it’s not already in requirements.txt
RUN pip install --no-cache-dir plotly

# Copy the current directory contents into the container at /app
COPY src/ ./


# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

