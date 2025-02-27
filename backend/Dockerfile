FROM python:3.11
WORKDIR /app
COPY . /app

COPY localhost.pem /app/localhost.pem
COPY localhost-key.pem /app/localhost-key.pem

RUN pip install --no-cache-dir -r requirements.txt
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--reload"]
CMD ["python", "manage.py", "runsslserver", "--certificate=localhost.pem", "--key=localhost-key.pem", "0.0.0.0:8000"]