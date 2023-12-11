#  <p align="center">📦 ELECTROSTOCK 📦</p>
## Descripción del Proyecto

Este repositorio alberga el código fuente y la documentación del Sistema de Gestión Integral, una plataforma compuesta por varios módulos para el seguimiento y administración eficiente de stocks, préstamos, cuentas, notificaciones y generación de informes. Este sistema está diseñado para proporcionar una solución completa y eficaz para la gestión de recursos y procesos, específicamente en el entorno de una institución educativa.

### Enfoque del Proyecto

El proyecto se fundamenta en tres pilares principales:
- **Control de Stock:** Se adoptó un enfoque similar al manejo de movimientos como un banco para una gestión eficiente.
- **Préstamos:** Incorpora elementos similares a plataformas conocidas como Mercado Libre para mejorar la experiencia de los usuarios.
- **Presupuesto:** Ofrece automatización y versatilidad en su uso para una gestión más eficiente de recursos.

## Módulos del Sistema

### 1. Sistema de Cuentas
Este módulo se enfoca en la administración de usuarios, sus permisos y funciones clave:
- Creación de usuarios desde múltiples formatos, incluyendo archivos Excel.
- Asignación sencilla de permisos.
- Proceso de registro para profesores con generación de tokens de acceso.
- Gestión y mantenimiento de cuentas y grupos.
- Seguridad y encriptación de tokens para su uso.
- Diferenciación de usuarios por especialidades y roles.
- Funcionalidades mejoradas de búsqueda, filtros y detalles de cuentas.

### 2. Sistema de Stock
El módulo de Control de Stock se ha diseñado para asegurar una gestión eficiente de recursos. Sus características clave incluyen:
- Carga y validación de modelos de especialidad.
- Alertas para productos con falta de stock.
- Importación y exportación de datos para una administración ágil.
- Proceso de exportación de datos sin elementos en lista negra.
- Uso de terminología en español para facilitar la comprensión.
- Implementación de backups semanales para emergencias.

### 3. Sistema de Préstamos
Diseñado para facilitar la gestión de préstamos, este módulo ofrece:
- Búsqueda y filtros de categorías.
- Carrito de compras operativo y seguimiento de préstamos.
- Gestión de aprobación y rechazo de préstamos.
- Seguimiento de préstamos vencidos y activos.
- Distintos estados para el proceso de préstamo.
- Validaciones de stock antes de préstamos.

### 4. Sistema de Notificaciones
Ofrece una comunicación efectiva entre usuarios con notificaciones específicas para diferentes roles.

### 5. Generación de Informes
Proporciona métricas y estadísticas valiosas para la toma de decisiones.

### 6. Aplicación Móvil
Ofrece acceso a las funcionalidades clave del sistema desde dispositivos móviles.

### 7. Presupuesto
Administración detallada de gastos y proyección de adquisiciones necesarias.

### 8. Diferenciación por Especialidad
Estructuración del proyecto para diferenciar y proporcionar herramientas específicas a cada área.

## Tecnologías Utilizadas
- Django/Python para el backend
- React/Javascript para el frontend
- Sqlite3 para la base de datos

## Instalación


### Configuración del Back-End (Django)

#### 1. Clonar el Repositorio

```bash
git clone https://github.com/tomasguell/FATG2-2023-VILLADA.git
cd FATG2-2023-VILLADA
```

#### 2. Crear un archivo `.env`
```bash
cd backend
python -m venv nombre_del_entorno
source nombre_del_entorno/bin/activate  # Unix
nombre_del_entorno\Scripts\activate     # Windows
pip install -r requirements.txt
```
#### 3. Configuración de la Base de Datos y Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
#### 4. Correr el Servidor Localmente
```bash
python manage.py runserver
```

### Configuración del Front-End (React)
#### 1. Instalar Node.js y Dependencias
```bash
cd frontend
npm install
```
#### 2. Iniciar el Proyecto
```bash
npm start
```

### Configuración de Celery
#### 1. Instalación y Configuración
```bash
pip install celery
```
#### 2. Iniciar Tareas en Segundo Plano con Celery
```bash
celery -A configura_tu_proyecto worker --loglevel=info
```


## Contacto

Si tienes preguntas o sugerencias, no dudes en contactarnos a través de [correo electrónico](correo@electronico.com).

¡Gracias por tu interés en ElectroStock!

