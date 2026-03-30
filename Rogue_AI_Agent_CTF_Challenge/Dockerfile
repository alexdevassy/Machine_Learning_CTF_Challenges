FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY .env .
COPY run_ctf.py .
COPY victim_app/ victim_app/
COPY marketplace/ marketplace/
COPY Images/ Images/

# Expose UI ports (agent APIs are internal)
EXPOSE 5000 5001

ENTRYPOINT ["python3", "run_ctf.py"]
