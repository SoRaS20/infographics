FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/app/

RUN mkdir -p /app/uploads/images /app/uploads/data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]