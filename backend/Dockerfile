FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--reload"]
CMD ["python", "manage.py", "runsslserver",
     "--certificate=localhost.crt",
     "--key=localhost.key",
     "0.0.0.0:8000"]