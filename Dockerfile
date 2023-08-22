# Utiliza una imagen base con Python
FROM python:3.9

#ENV
ENV SECRET_KEY os.environ.get('DJANGO_SECRET_KEY')
ENV DATABASE_NAME 'postgres'
ENV DATABASE_USER 'pfsatuser'
ENV DATABASE_PASSWORD 'pfsatpassword'
ENV DATABASE_HOST 'pfsat.cyx88m3smqeb.sa-east-1.rds.amazonaws.com'
ENV DATABASE_PORT 5432
ENV EMAIL_USER 'proyectofinalsat@gmail.com'
ENV EMAIL_PASSWORD 'vejlablgiwzskngh'

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos al directorio de trabajo
COPY requirements.txt /app/

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del directorio actual al directorio de trabajo
COPY . /app/

# Exponer el puerto en el que se ejecutará el servidor de Django
EXPOSE 8000

# Comando para ejecutar la migracion de la db
CMD ["python", "manage.py", "migrate"]

# Comando para ejecutar el servidor de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]