nombre y descripción del proyecto: API de Usuarios y Habitaciones

- API de Usuarios y Habitaciones. 
hice dos API con FastAPI: una para administrar usuarios y otra para administrar habitaciones. Con ellas podemos registrar, consultar, actualizar y eliminar información en cada una.

Objetivo:

el objetivo es permitir que podamos gestionar los usuarios y las habitaciones por medio de solicitudes HTTP. También podemos validar la información antes de guardarla en la base de datos.

módulos desarrollados:

-en el proyecto trabajamos con estos archivos y carpetas:

- usuario.py: aquí tenemos las operaciones para registrar, consultar, actualizar y eliminar usuarios.
- habitacion.py: aquí podemos registrar, consultar, actualizar y eliminar habitaciones. También podemos buscar habitaciones según su tipo.
- database.py: configuramos la conexión con la base de datos.
- usuarios/model/models.py: definimos los campos que tiene la tabla de usuarios.
- usuarios/schema/schemas.py: validamos la información que recibimos y enviamos de los usuarios.
- usuarios/security.py: tenemos una función para generar un hash de contraseña.
- habitaciones/model/models.py: definimos los campos de la tabla de habitaciones.
- habitaciones/schema/schemas.py: validamos los datos de las habitaciones.

Arquitectura por capas:

- se conecta con swagger o el cliente
- luego hace conexion con la API de Usuarios y de Habitaciones
- despues de eso los datos que se ingresen en las dos API, se iran hacia la base de datos y se guardan en las tablas
- se valida que los datos tenga un formato correcto
- finalmente los datos y las tablas se veran desde el gestor de datos NEON

enpoints utilizados para las dos API:

- GET = consultar registros
- GET = con el id (consulta un registro en especifico)
- POST = creamos un registro
- PUT = actualizamos un registro
- DELETE = borramos un registro

pruebas de swagger:

- se evidencia delante del instructor al momento de sustentar

utilizacion de NEON:

en database.py configuramos la conexión con sqlalchemmy. La dirección de la base de datos se obtiene desde la variable DATABASE_URL, que guardamos en el archivo .env

ejemplo de configuración:

DATABASE_URL=postgresql+psycopg://USUARIO:CONTRASEÑA@HOST/BASE_DE_DATOS?sslmode=require

