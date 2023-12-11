from celery import shared_task
from django.utils import timezone
from .models import *
from django.core.mail import send_mail
import logging
from django.contrib.auth.models import Group



@shared_task
def run_check_expired_logs():
    print("pase")
    now = timezone.now()
    approved_logs = Log.objects.filter(status="AP")

    for log in approved_logs:
        lender = None
        if log.dateOut is not None and log.dateOut < now:
            log.status = "VEN"
            log.save()
            logging.info(f"Se cambio el estado del log")
            lender = log.lender
            if lender is not None:
                send_notification_email(lender.email)



def send_notification_email(mail):
    print("se envio el mail")
    subject = "Tu prestamo se ha vencido"
    message = "Estimado alumno,\n\nTu préstamo ha vencido. Por favor, devuélvelo a la brevedad.\n\nSaludos,\nInstituto Tecnico Salesiano Villada"
    sender_email = (
        "deniva4297@anwarb.com"  # Dirección de correo electrónico del remitente
    )

    send_mail(subject, message, sender_email, [mail])


@shared_task
def assign_next_year_course():
    current_year = timezone.now().year
    logging.info(f"Current year: {current_year}")

    alumno_group = Group.objects.get(name="Alumno")

    for user in CustomUser.objects.all():
        user_registration_year = user.date_joined.year
        years_since_registration = current_year - user_registration_year + 4
        logging.info(f"years_since_registration: {years_since_registration}")

        if years_since_registration > 3 and alumno_group in user.groups.all():
            next_year = current_year - user_registration_year + 4
            try:
                next_year_course = Course.objects.get(grade=next_year)
                user.course = next_year_course
                user.save()
                logging.info(
                    f"Assigned course for next year to user {user.username}: {next_year_course}"
                )
            except Course.DoesNotExist:
                logging.warning(f"No course found for year {next_year}")
                user.delete()  # Eliminar el usuario si el curso no existe

from django.core.management import call_command
from celery import shared_task
from django.core.management import call_command
import os
import datetime

@shared_task
def backup_database():
    try:
        # Ejecuta el comando dumpdata para exportar los datos de la base de datos
        # Obtener la fecha de hoy
        fecha_hoy = datetime.datetime.now().strftime('%Y-%m-%d')  # Formato: Año-Mes-Día

        # Nombre del archivo de copia de seguridad con la fecha de hoy
        backup_filename = f'backup_data_{fecha_hoy}.json'
        call_command('dumpdata', output=backup_filename)

        # Mueve el archivo de copia de seguridad a un directorio específico
        backup_directory = '../Backups/'  # Reemplaza con tu directorio de backups
        os.rename(backup_filename, os.path.join(backup_directory, backup_filename))
    except Exception as e:
        # Maneja cualquier excepción que pueda ocurrir durante el respaldo
        raise e
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

@shared_task
def check_stock_and_add_budget_logs():
    # Obtén todos los productos que tengan un stock mínimo
    products_with_minimum_stock = Box.objects.filter(minimumStock__isnull=False)

    for product in products_with_minimum_stock:
        # Verificar si ya existe un registro de presupuesto para este elemento
        existing_budget_log = BudgetLog.objects.filter(element__name=product.element.name).first()



        # Recupera el elemento correspondiente al producto
        element_instance = product.element

        # Calcular la cantidad total de registros de préstamos con estado 'COM' para el elemento actual
        borrowed_logs_com = Log.objects.filter(box__element=element_instance, status='COM').aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Calcular la cantidad total de registros de préstamos con estado 'ROTO' para el elemento actual
        borrowed_logs_roto = Log.objects.filter(box__element=element_instance, status='ROT').aggregate(Sum('quantity'))['quantity__sum'] or 0

        # Calcula la cantidad a agregar como la diferencia entre los préstamos 'COM' y los préstamos 'ROTO'
        quantity_to_add =  product.minimumStock  -(borrowed_logs_com - borrowed_logs_roto)
        # Encuentra la especialidad siguiendo la cadena de relaciones desde Box
        speciality = None
        if element_instance:
            try:
                location = product.location
                laboratory = location.laboratoy
                speciality = laboratory.speciality
            except (Location.DoesNotExist, Laboratory.DoesNotExist, Speciality.DoesNotExist):
                pass

        # Encuentra el último presupuesto para la especialidad del producto, si existe
        latest_budget = None
        if speciality:
            try:
                latest_budget = Budget.objects.filter(speciality=speciality).latest('id')
            except Budget.DoesNotExist:
                pass

        # Calcula la cantidad a agregar como la diferencia entre el stock mínimo y el stock actual

        logging.info(
                    f"cantidad a agregar: {quantity_to_add}, comprado: {borrowed_logs_com}, roto: {borrowed_logs_roto}, srock minimo: {product.minimumStock }"
                )

        if existing_budget_log:
            # Actualizar la cantidad en el registro de presupuesto existente
            existing_budget_log.quantity = quantity_to_add
            existing_budget_log.save()
        else:
            if quantity_to_add > 0:
                # Agregar un nuevo BudgetLog con los detalles
                budget_log = BudgetLog.objects.create(
                    name='',
                    status='PENDIENTE',
                    price=0,
                    element=element_instance,
                    budget=latest_budget,
                    quantity=quantity_to_add,
                )





