import csv
from django.shortcuts import render
from .models import *
from django.contrib.auth.models import Group


def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            # Obtener la especialidad del usuario desde el archivo CSV y buscarla en la base de datos
            specialty_name = row['Especialidad']
 
            
            # Buscar el curso correspondiente para la especialidad y el año 4
            course = Course.objects.filter(number='4')
           
            #print('Year:',year)
            course = Course.objects.filter(number=1).first()
            if not course:
                continue  # Si no se encuentra un curso, saltar a la siguiente fila
            
            # Crear el usuario y asignarle el curso y la especialidad correspondientes
            user = CustomUser(
                first_name=row['Nombre'],
                last_name=row['Apellido'],
                email=row['Mail'],
                username=row['Nombre']+ row['Apellido'],
                password=row['DNI'],
                course=course,
                speciality=specialty_name
            )
            user.save()

            #asignar grupo
            alumno_group = Group.objects.get(name='Alumno')
            user.groups.add(alumno_group)

        return render(request, 'upload_csv.html', {'success': True})
    return render(request, 'upload_csv.html')
