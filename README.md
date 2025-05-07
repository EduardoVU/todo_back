# todo_back

Este proyecto es una API de backend para una aplicación de gestión de tareas (todo list). Está desarrollado en **FastAPI** y utiliza una base de datos **MySQL**. El proyecto incluye autenticación, gestión de usuarios, y CRUD de tareas.

## Tecnologías

- **FastAPI**: Framework para desarrollar APIs de forma rápida y eficiente.
- **Pydantic**: Utilizado para la validación de datos y serialización de modelos (ORM).
- **SQLAlchemy**: ORM para la interacción con la base de datos MySQL.
- **Alembic**: Herramienta para la gestión de migraciones de bases de datos.
- **Bcrypt**: Para el hash de contraseñas de forma segura.
- **JWT (JSON Web Token)**: Para la autenticación basada en tokens.
- **OAuth2**: Protocolo para la autorización de acceso.

## Requerimientos

- **MySQL**: Necesitas tener una base de datos MySQL configurada.
- **Archivo `.env`**: Asegúrate de tener configurado tu archivo `.env` con las variables necesarias para la conexión y la autenticación.

## Configuración

1. Copia el archivo `.env.example` a `.env`.
2. Configura las siguientes variables en el archivo `.env`:
   
## Ejemplo de .env

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
DB_NAME=your_db_name


Asegúrate de que estas variables apunten a tu configuración correcta de base de datos y claves de seguridad.

## Comandos

### Instalar dependencias

Para instalar todas las dependencias del proyecto, ejecuta el siguiente comando:

pip install -r requirements.txt

### Generar archivo `requirements.txt` con nuevas dependencias

Si agregas nuevas dependencias al proyecto, puedes generar un archivo `requirements.txt` actualizado con:

pip freeze > requirements.txt

### Correr el proyecto

Para iniciar el servidor de desarrollo en FastAPI, ejecuta:

uvicorn main:app --reload --port 3000

Si es necesario cambiar el puerto en el que correrá el proyecto, cambiarlo en el comando

### Migraciones

#### Hacer migraciones:

1. Crear una nueva migración:

alembic revision --autogenerate -m "tu mensaje"


2. Aplicar la migración para actualizar la base de datos:

alembic upgrade head


#### Deshacer migraciones:

Para revertir la última migración, usa:

alembic downgrade -1


### Crear tablas en la base de datos

Una vez configurado el archivo `.env` y con la base de datos MySQL corriendo, crea las tablas utilizando Alembic:

alembic upgrade head


### Pendientes
Mandar a correo el código de autenticación al correo
Mandar a login cuando expire el token
Cookies de login
Poner la carpeta dist del front en el backend para subir un solo proyecto a producción, o bien, tener dos terminales, una con el front y otra con el back

