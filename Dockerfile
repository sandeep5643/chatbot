FROM python:3.10.11-slim

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt .

# ⏳ heavy install → single worker later
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "1", "-t", "180", "--preload", "-b", "0.0.0.0:5000", "app:app"]
