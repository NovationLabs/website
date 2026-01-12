FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn jinja2 psutil python-dotenv aiofiles

EXPOSE 9998

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9998"]
