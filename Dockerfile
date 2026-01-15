# 🔹 Python 3.8.10 base image
FROM python:3.8.10-slim

# 🔹 Set working directory
WORKDIR /app

# 🔹 Copy requirements first
COPY requirements.txt .

# 🔹 Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🔹 Copy full project
COPY . .

# 🔹 Expose port
EXPOSE 5000

# 🔹 Environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# 🔹 Run app with Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
