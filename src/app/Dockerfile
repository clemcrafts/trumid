FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r src/app/requirements.txt

EXPOSE 80

CMD ["python", "-m", "src.app.run"]