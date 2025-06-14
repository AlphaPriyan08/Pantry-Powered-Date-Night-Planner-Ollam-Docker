# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container at /app
COPY . .

# Make port 8501 available to the world outside this container
# This is the default port for Streamlit
EXPOSE 8501

# Define the command to run your app
# This will run `streamlit run app.py` when the container launches
# Make sure 'app.py' is the name of your main script
CMD ["streamlit", "run", "app.py"]