FROM python:3.8-bullseye

WORKDIR /ElectroStock

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate || echo "Migration failed"

EXPOSE 8000

CMD ["gunicorn","ElectroStock.wsgi:application"]