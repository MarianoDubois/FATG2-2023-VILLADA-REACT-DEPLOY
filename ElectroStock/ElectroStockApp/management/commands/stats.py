from django.core.management.base import BaseCommand
from ElectroStockApp.models import Speciality, Laboratory, Course, Category, Element


class Command(BaseCommand):
    help = 'Carga de datos iniciales en la base de datos'

    def handle(self, *args, **options):
        # Agregar cursos
        grades = [4, 5, 6, 7]
        for grade in grades:
            course, created = Course.objects.get_or_create(grade=grade)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Curso {grade} creado exitosamente."))
            else:
                self.stdout.write(f"Dato ya existente")

        # Agregar especialidades
        specialities = ['electronica', 'programacion', 'electromecanica']
        for speciality in specialities:
            speciality_obj, created = Speciality.objects.get_or_create(name=speciality)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Especialidad {speciality} creada exitosamente."))
            else:
                self.stdout.write(f"Dato ya existente")

        # Agregar laboratorios
        lab_data = [
            {'name': 'Laboratorio 1', 'speciality': 'electronica'},
            {'name': 'Laboratorio 2', 'speciality': 'electronica'}
        ]
        for data in lab_data:
            speciality = speciality = Speciality.objects.get(name=data['speciality'])
            lab, created = Laboratory.objects.get_or_create(name=data['name'], speciality=speciality)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Laboratorio '{data['name']}' creado exitosamente."))
            else:
                self.stdout.write(f"Dato ya existente")

        
        #DATOS DE EJEMPLO:
        # Check if the first element exists
        if not Element.objects.filter(name="Elemento 1").exists():
            # Crea categorías
            categoria1 = Category.objects.create(name="Categoría 1", description="Descripción de la categoría 1")
            categoria2 = Category.objects.create(name="Categoría 2", description="Descripción de la categoría 2")
            # Agrega más categorías aquí si es necesario

            # Crea elementos
            elemento1 = Element.objects.create(name="Elemento 1", description="Descripción del elemento 1",  price_usd=10.99, category=categoria1)
            elemento2 = Element.objects.create(name="Elemento 2", description="Descripción del elemento 2", price_usd=5.99, category=categoria1)
            elemento3 = Element.objects.create(name="Elemento 3", description="Descripción del elemento 3", price_usd=7.99, category=categoria2)
            elemento4 = Element.objects.create(name="Elemento 4", description="Descripción del elemento 4",  price_usd=12.99, category=categoria2)
            elemento5 = Element.objects.create(name="Elemento 5", description="Descripción del elemento 5",  price_usd=8.99, category=categoria1)
            elemento6 = Element.objects.create(name="Elemento 6", description="Descripción del elemento 6", price_usd=9.99, category=categoria2)
            elemento7 = Element.objects.create(name="Elemento 7", description="Descripción del elemento 7",  price_usd=11.99, category=categoria1)
            elemento8 = Element.objects.create(name="Elemento 8", description="Descripción del elemento 8", price_usd=6.99, category=categoria2)
            elemento9 = Element.objects.create(name="Elemento 9", description="Descripción del elemento 9", price_usd=14.99, category=categoria1)
            elemento10 = Element.objects.create(name="Elemento 10", description="Descripción del elemento 10",  price_usd=7.99, category=categoria2)
            elemento11 = Element.objects.create(name="Elemento 11", description="Descripción del elemento 11", price_usd=9.99, category=categoria1)
            elemento12 = Element.objects.create(name="Elemento 12", description="Descripción del elemento 12", price_usd=13.99, category=categoria2)
            elemento13 = Element.objects.create(name="Elemento 13", description="Descripción del elemento 13",  price_usd=10.99, category=categoria1)
            elemento14 = Element.objects.create(name="Elemento 14", description="Descripción del elemento 14", price_usd=8.99, category=categoria2)
            elemento15 = Element.objects.create(name="Elemento 15", description="Descripción del elemento 15",  price_usd=11.99, category=categoria1)
            elemento16 = Element.objects.create(name="Elemento 16", description="Descripción del elemento 16", price_usd=9.99, category=categoria2)
            elemento17 = Element.objects.create(name="Elemento 17", description="Descripción del elemento 17",  price_usd=12.99, category=categoria1)
            elemento18 = Element.objects.create(name="Elemento 18", description="Descripción del elemento 18", price_usd=7.99, category=categoria2)
            elemento19 = Element.objects.create(name="Elemento 19", description="Descripción del elemento 19", price_usd=14.99, category=categoria1)
            elemento20 = Element.objects.create(name="Elemento 20", description="Descripción del elemento 20",  price_usd=6.99, category=categoria2)
            elemento21 = Element.objects.create(name="Elemento 21", description="Descripción del elemento 21",  price_usd=10.99, category=categoria1)
            elemento22 = Element.objects.create(name="Elemento 22", description="Descripción del elemento 22", price_usd=5.99, category=categoria1)
            elemento23 = Element.objects.create(name="Elemento 23", description="Descripción del elemento 23", price_usd=7.99, category=categoria2)
            elemento24 = Element.objects.create(name="Elemento 24", description="Descripción del elemento 24",  price_usd=12.99, category=categoria2)
            elemento25 = Element.objects.create(name="Elemento 25", description="Descripción del elemento 25",  price_usd=8.99, category=categoria1)
            elemento26 = Element.objects.create(name="Elemento 26", description="Descripción del elemento 26", price_usd=9.99, category=categoria2)
            elemento27 = Element.objects.create(name="Elemento 27", description="Descripción del elemento 27",  price_usd=11.99, category=categoria1)
            elemento28 = Element.objects.create(name="Elemento 28", description="Descripción del elemento 28", price_usd=6.99, category=categoria2)
            elemento29 = Element.objects.create(name="Elemento 29", description="Descripción del elemento 29", price_usd=14.99, category=categoria1)
            elemento30 = Element.objects.create(name="Elemento 30", description="Descripción del elemento 30",  price_usd=7.99, category=categoria2)
            elemento31 = Element.objects.create(name="Elemento 31", description="Descripción del elemento 31", price_usd=9.99, category=categoria1)
            elemento32 = Element.objects.create(name="Elemento 32", description="Descripción del elemento 32", price_usd=13.99, category=categoria2)
            elemento33 = Element.objects.create(name="Elemento 33", description="Descripción del elemento 33",  price_usd=10.99, category=categoria1)
            elemento34 = Element.objects.create(name="Elemento 34", description="Descripción del elemento 34", price_usd=8.99, category=categoria2)
            elemento35 = Element.objects.create(name="Elemento 35", description="Descripción del elemento 35",  price_usd=11.99, category=categoria1)
            elemento36 = Element.objects.create(name="Elemento 36", description="Descripción del elemento 36", price_usd=9.99, category=categoria2)
            elemento37 = Element.objects.create(name="Elemento 37", description="Descripción del elemento 37",  price_usd=12.99, category=categoria1)
            elemento38 = Element.objects.create(name="Elemento 38", description="Descripción del elemento 38", price_usd=7.99, category=categoria2)
            elemento39 = Element.objects.create(name="Elemento 39", description="Descripción del elemento 39", price_usd=14.99, category=categoria1)
            elemento40 = Element.objects.create(name="Elemento 40", description="Descripción del elemento 40",  price_usd=6.99, category=categoria2)
            elemento41 = Element.objects.create(name="Elemento 41", description="Descripción del elemento 41",  price_usd=10.99, category=categoria1)
            elemento42 = Element.objects.create(name="Elemento 42", description="Descripción del elemento 42", price_usd=5.99, category=categoria1)
            elemento43 = Element.objects.create(name="Elemento 43", description="Descripción del elemento 43", price_usd=7.99, category=categoria2)
            elemento44 = Element.objects.create(name="Elemento 44", description="Descripción del elemento 44",  price_usd=12.99, category=categoria2)
            elemento45 = Element.objects.create(name="Elemento 45", description="Descripción del elemento 45",  price_usd=8.99, category=categoria1)
            elemento46 = Element.objects.create(name="Elemento 46", description="Descripción del elemento 46", price_usd=9.99, category=categoria2)
            elemento47 = Element.objects.create(name="Elemento 47", description="Descripción del elemento 47",  price_usd=11.99, category=categoria1)
            elemento48 = Element.objects.create(name="Elemento 48", description="Descripción del elemento 48", price_usd=6.99, category=categoria2)
            elemento49 = Element.objects.create(name="Elemento 49", description="Descripción del elemento 49", price_usd=14.99, category=categoria1)
            elemento50 = Element.objects.create(name="Elemento 50", description="Descripción del elemento 50",  price_usd=7.99, category=categoria2)
            print("elementos y categorias de ejemplo creados")
        else:
            print("datos de ejemplo ya existentes")