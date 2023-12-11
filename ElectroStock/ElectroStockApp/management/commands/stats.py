from django.core.management.base import BaseCommand
from ElectroStockApp.models import Speciality, Laboratory, Course, Category, Element, Location, TokenSignup
from django.contrib.auth import get_user_model

User = get_user_model()
class Command(BaseCommand):
    help = 'Carga de datos iniciales en la base de datos'

    def handle(self, *args, **options):

        # Agregar especialidades
        specialities = ['electronica', 'programacion', 'electromecanica']
        for speciality in specialities:
            speciality_obj, created = Speciality.objects.get_or_create(name=speciality)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Especialidad {speciality} creada exitosamente."))
            else:
                self.stdout.write(f"Dato especialidad ya existente")
                
        #users
        especialidad_electronica = Speciality.objects.get(name='electronica')
        usuarios_data = [
            {'username': 'Michalik', 'especialidad': especialidad_electronica},
            {'username': 'Vettorello', 'especialidad': especialidad_electronica},
            {'username': 'Córdoba', 'especialidad': especialidad_electronica},
            {'username': 'Remedi', 'especialidad': especialidad_electronica},
        ]

        for usuario_data in usuarios_data:
            username = usuario_data['username']
            especialidad = usuario_data['especialidad']

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username)
                user.specialties.add(especialidad)
                user.save()
                print('Usuario creado')


        # Categorias padre
        equipos, _ = Category.objects.get_or_create(name='equipos')
        componentes, _ = Category.objects.get_or_create(name='componentes')
        insumos, _ = Category.objects.get_or_create(name='insumos')
        maletines_componentes, _ = Category.objects.get_or_create(name='maletines componentes')
        kits_arduino, _ = Category.objects.get_or_create(name='kits arduino')
        maletines, _ = Category.objects.get_or_create(name='maletines')
        lockers, _ = Category.objects.get_or_create(name='lockers')
        armario, _ = Category.objects.get_or_create(name='armario')
        repuestos, _ = Category.objects.get_or_create(name='repuestos')
        
        
        # Agregar cursos
        grades = [4, 5, 6, 7]
        for grade in grades:
            course, created = Course.objects.get_or_create(grade=grade)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Curso {grade} creado exitosamente."))
            else:
                self.stdout.write(f"Dato curso ya existente")

        # Agregar laboratorios
        lab_data = [
            {'name': 'Laboratorio 1', 'speciality': 'electronica'},
            {'name': 'Laboratorio 2', 'speciality': 'electronica'}
        ]
        for data in lab_data:
            speciality = Speciality.objects.get(name=data['speciality'])
            lab, created = Laboratory.objects.get_or_create(name=data['name'], speciality=speciality)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Laboratorio '{data['name']}' creado exitosamente."))
            else:
                self.stdout.write(f"Dato laboratorio ya existente")

        # Categorias hijas
        sensores, _ = Category.objects.get_or_create(name='sensores', category=equipos)
        
        categorias_componentes = [
            'resistencias',
            'lamparas e indicadores',
            'diodos y rectificadores',
            'opticos y displays',
            'transistores',
            'tiristores',
            'parlantes y microfonos',
            'inductancias, nucleos y transformadores',
            'capacitores',
            'interruptores, pulsadores y reles',
            'buffers',
            'ci digitales',
            'cristales y osciladores',
            'zocalos',
            'ci transmisores, receptores y modulos',
            'reguladores de tension y protecciones',
            'ci analogicos',
            'conectores, borneras, terminales y fichas',
            'elementos disipadores y aisladores',
            'fusibles y portafusibles',
            'elementos de montaje',
            'motores y servomecanismos',
            'cables varios'
        ]
        for categoria in categorias_componentes:
            Category.objects.get_or_create(name=categoria, category=componentes)

        categorias_insumos = [
            'informatica',
            'electricidad/electronica',
            'ferreteria',
            'libreria',
            'impresión 3d',
            'drogueria - quimica',
            'proceso fabricacion circuitos impresos'
        ]
        for categoria in categorias_insumos:
            Category.objects.get_or_create(name=categoria, category=insumos)

        categorias_maletines_componentes = [
            'cables',
            'potenciómetros',
            'varios',
            'diodos',
            'resistencias maletines componentes',
            'capacitores electrolíticos',
            'capacitores varios'
        ]

        for categoria in categorias_maletines_componentes:
            Category.objects.get_or_create(name=categoria, category=maletines_componentes)

        self.stdout.write(self.style.SUCCESS('Datos categorias ya creados'))


        data = [
            (1, "A1", 1),
            (2, "M5", 1),
            (3, "A2", 1),
            (4, "Depósito", 1),
            (5, "A3", 1),
            (6, "C1-C5", 1),
            (7, "C3", 1),
            (8, "Caja htas", 1),
            (9, "D7", 1),
            (10, "Estante", 1),
            (11, "Laboratorio", 1),
            (12, "M1", 1),
            (13, "M1- M5 ", 1),
            (14, "M1-M12", 1),
            (15, "M1-M6 y A2", 1),
            (16, "M2", 1),
            (17, "M3", 1),
            (18, "M6 ", 1),
            (19, "M4", 1),
            (20, "M6 - M12", 1),
            (21, "M7-M12", 1),
            (22, "Mesa 13 LAB 1", 1),
            (23, "Mesa 13 - Caja htas", 1),
            (24, "Mesa 14 LAB 1", 1),
            (25, "Mesas", 1),
            (26, "Mesas - Cajón Herramientas", 1),
            (27, "Mesas - Cajón Programación", 1),
            (28, "Mesas 1-12", 1),
            (29, "C2", 1),
            (30, "C1", 1),
            (31, "C4", 1),
            (32, "D13", 1),
            (33, "D14", 1),
            (34, "C5", 1),
            (35, "Caja htas+A3", 1),
            (36, "M13", 1),
            (37, "M14", 1),
            (38, "Laboratorio 1", 1),
            (39, "LAB 1", 1),
            (40, "LAB 2", 2),
            (41, "M1 - M12", 2),
            (42, "Mesa 13 LAB 2", 2),
            (43, "Mesa de perforación", 2),
            (44, "Maletin inductivo M14", 2),
            (45, "Maletin capacitivo M14", 2),
            (46, "Maletin M14", 2),
            (47, "Mesa 14 LAB 2", 2),
            (48, "Maqueta tablero amarillo", 2),
            (49, "Mesa mármol", 2),
            (50, "Laboratorio 2", 2),
            (51, "Sector ELEC. IND.2", 2),
            (52, "Sector ELEC.IND.2", 2),
            (53, "Sector INF.ELEC.2", 2),
            (54, "Cajón", 2),
            (55, "Sector ELECTROTEC.2", 2)
        ]
        for id, name, laboratory_id in data:
            laboratory = Laboratory.objects.get(id=laboratory_id)
            
            # Actualiza o crea la ubicación usando el ID especificado
            location, created = Location.objects.update_or_create(
                id=id,
                defaults={'name': name, 'laboratoy': laboratory}
            )

            if created:
                print(f"Ubicación creada: {id}")


        token, _ = TokenSignup.objects.get_or_create(name='villada')
