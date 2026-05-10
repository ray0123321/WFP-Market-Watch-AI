# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the model and code files
COPY . .

# Expose the port FastAPI runs on
EXPOSE 7860

# Command to run the server on Hugging Face (port 7860 is mandatory for HF)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
