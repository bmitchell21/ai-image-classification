# Official lightweight Python image
FROM python:3.8-slim

# Working directory in the container
WORKDIR /app

# Copy the required files to the working directory
COPY app/python .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available outside this container
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]