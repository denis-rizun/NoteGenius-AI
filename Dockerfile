FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONPATH=/app/src

EXPOSE 8001

CMD ["uvicorn", "src.backend.api:app", "--host", "0.0.0.0", "--port", "8001"]
