import csv
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .models import Specialty

User = get_user_model()

def process_csv(file):
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    for row in reader:
        try:
            user = User.objects.get(username=row['DNI'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(
                username=row['DNI'],
                first_name=row['Nombre'],
                last_name=row['Apellido'],
                email=row['Mail']
            )
        try:
            user.speciality = Specialty.objects.get(name=row['Especialidad'])
        except ObjectDoesNotExist:
            pass
        user.save()

