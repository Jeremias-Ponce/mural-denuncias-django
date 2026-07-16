# Usamos una versión ligera de Python
FROM python:3.12-slim

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos la lista de herramientas y las instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el resto del proyecto
COPY . .

# El comando que ejecutará Docker para arrancar la página
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]