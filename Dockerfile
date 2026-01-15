# =========================
# Base Image (Python 3.10.11)
# =========================
FROM python:3.10.11-slim

# =========================
# Environment variables
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# Set work directory
# =========================
WORKDIR /app

# =========================
# Install system dependencies
# (faiss, torch, numpy ke liye required)
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Upgrade pip (IMPORTANT)
# =========================
RUN python -m pip install --upgrade pip

# =========================
# Copy & install dependencies
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# Copy full project
# =========================
COPY . .

# =========================
# Expose port (Render / Local)
# =========================
EXPOSE 5000

# =========================
# Start app with Gunicorn
# =========================
CMD ["gunicorn", "-w", "1", "--timeout", "120", "-b", "0.0.0.0:5000", "app:app"]
