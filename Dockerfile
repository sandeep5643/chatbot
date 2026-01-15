FROM python:3.10.11-slim

WORKDIR /app

# 🔥 ONLY upgrade pip (no apt-get)
RUN python -m pip install --upgrade pip

COPY requirements.txt .

# ⚠️ This will still take time but will NOT crash
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-t", "120", "-b", "0.0.0.0:5000", "app:app"]
