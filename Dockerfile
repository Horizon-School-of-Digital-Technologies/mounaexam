FROM python:3.10.12

WORKDIR /app

copy requirements.txt .

run pip3 install -r requirements.txt

COPY app.py .

EXPOSE 5000

ENTRYPOINT ["python","app.py"]
