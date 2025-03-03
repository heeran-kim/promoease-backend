FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Ensure the script is executable
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver_plus", "--cert-file", "/app/localhost.pem", "--key-file", "/app/localhost-key.pem", "0.0.0.0:8000"]