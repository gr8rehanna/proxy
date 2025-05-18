## Create docker file to run this app in docker using python3.12 and start app.py
#FROM python:3.12.10-alpine
FROM python:3.11.9-bullseye
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
EXPOSE 8080
CMD ["python", "main.py"]