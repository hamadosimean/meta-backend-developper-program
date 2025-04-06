FROM python:3

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD ["python3","manage.py","runserver","127.0.0.1:8000"]