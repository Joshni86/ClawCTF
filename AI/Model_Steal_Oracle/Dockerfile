FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app", "--workers", "2", "--threads", "4", "--timeout", "30"]
