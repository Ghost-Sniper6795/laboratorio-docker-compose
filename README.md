\# Laboratorio: Despliegue de una aplicación web con Docker Compose



\*\*Alumno:\*\* Pablo Castro  

\*\*Ciclo formativo:\*\* 2.º ASIR  

\*\*Módulo:\*\* Administración de Sistemas Informáticos en Red



\---



\## 1. Descripción del proyecto



En este laboratorio hemos desplegado una aplicación web para la gestión de incidencias utilizando Docker Compose.



La aplicación está formada por tres servicios independientes:



\- \*\*Frontend:\*\* interfaz web desarrollada en HTML y servida mediante Nginx.

\- \*\*Backend:\*\* API desarrollada en Python con Flask, encargada de procesar las peticiones y comunicarse con la base de datos.

\- \*\*PostgreSQL:\*\* sistema gestor de bases de datos donde se almacenan las incidencias registradas.



La arquitectura utiliza dos redes internas de Docker y un volumen persistente para conservar la información de PostgreSQL.



\## 2. Preguntas y respuestas



\### 1. ¿Por qué el frontend no necesita conectarse a PostgreSQL?



El frontend no necesita conectarse directamente a PostgreSQL porque su función es mostrar la página web y permitir que los usuarios interactúen con ella. Las consultas y operaciones con la base de datos las realiza el backend, que se encarga de gestionar la información y comunicarse con PostgreSQL. De esta manera, evitamos exponer la base de datos directamente al usuario.



\### 2. ¿Por qué el backend pertenece a dos redes?



El backend pertenece a dos redes porque necesita comunicarse tanto con el frontend como con PostgreSQL. Una red permite la comunicación entre el frontend y el backend, mientras que la otra permite que el backend acceda a la base de datos. Así se mantiene una separación entre los servicios.



\### 3. ¿Qué servicio necesita publicar un puerto en el anfitrión?



El frontend necesita publicar un puerto en el anfitrión para que podamos acceder a la aplicación desde el navegador de nuestro ordenador. En nuestra configuración utilizamos el puerto 8080 del anfitrión, que se conecta con el puerto 80 del contenedor Nginx. Los demás servicios se comunican internamente mediante las redes de Docker.



\### 4. ¿Por qué publicar PostgreSQL hacia fuera no es la solución adecuada para un fallo de comunicación interno?



Porque si el backend y PostgreSQL no se comunican, lo correcto es revisar la configuración de las redes internas, los nombres de los servicios y los puertos. Publicar PostgreSQL hacia fuera no soluciona el problema y además puede crear un riesgo de seguridad al permitir conexiones externas a la base de datos.



\### 5. ¿Qué ventaja ofrece Docker Compose respecto a ejecutar los tres contenedores manualmente?



Docker Compose permite gestionar todos los servicios desde un único archivo de configuración. Podemos iniciar, detener y reconstruir los contenedores con pocos comandos, sin tener que configurar cada uno por separado. También facilita que toda la aplicación mantenga la misma configuración y que los servicios se comuniquen correctamente.



\### 6. ¿Por qué hemos dividido la arquitectura en dos redes?



Hemos dividido la arquitectura en dos redes para separar las comunicaciones de la aplicación. Por un lado, tenemos la red del frontend y el backend, y por otro, la red del backend y PostgreSQL. Esto mejora la organización, reduce las conexiones innecesarias y proporciona una mayor seguridad al evitar que el frontend tenga acceso directo a la base de datos.



\### 7. ¿Por qué el backend utiliza `db` como dirección de PostgreSQL?



Porque Docker Compose proporciona resolución DNS interna entre los servicios que comparten una misma red. El nombre `db` corresponde al nombre del servicio de PostgreSQL definido en el archivo `compose.yaml`. Por eso el backend puede localizar la base de datos utilizando ese nombre, sin necesitar una dirección IP fija.



\### 8. ¿Qué diferencia existe entre detener un proyecto y eliminar sus volúmenes?



Detener y eliminar los contenedores de un proyecto con `docker compose down` elimina los contenedores y las redes creadas para la aplicación, pero conserva los volúmenes con nombre. En cambio, al utilizar `docker compose down -v`, también se eliminan los volúmenes del proyecto y, con ellos, los datos almacenados en PostgreSQL.



\### 9. ¿Qué consecuencias tendría para la empresa perder el volumen de PostgreSQL?



La empresa podría perder toda la información almacenada en la base de datos, incluyendo las incidencias registradas y otros datos importantes de la aplicación. Esto supondría una pérdida de información, problemas para continuar trabajando y posiblemente un perjuicio económico. Por eso es importante conservar los volúmenes y realizar copias de seguridad periódicas.



\---



\## 3. Estructura de la arquitectura



La aplicación utiliza la siguiente distribución:



\- \*\*red\_frontend:\*\* conecta el frontend con el backend.

\- \*\*red\_database:\*\* conecta el backend con PostgreSQL.

\- \*\*postgres\_data:\*\* volumen persistente donde se almacenan los datos de PostgreSQL.



El backend utiliza el nombre `db` para comunicarse con PostgreSQL mediante la red interna de Docker.



\## 4. Comprobaciones realizadas



Se ha comprobado el funcionamiento de los servicios mediante Docker Compose:



\- Comprobación de la configuración con `docker compose config`.

\- Construcción e inicio de los servicios con `docker compose up -d --build`.

\- Comprobación del estado de los contenedores con `docker compose ps`.

\- Consulta de los registros mediante `docker compose logs`.

\- Acceso a la aplicación desde el navegador mediante `http://localhost:8080`.

\- Prueba de registro y visualización de incidencias.



También se ha comprobado que los datos permanecen almacenados después de detener y volver a iniciar el proyecto, gracias al volumen persistente de PostgreSQL.



\## 5. Conclusión



Con esta práctica hemos aprendido a desplegar una aplicación web formada por varios servicios utilizando Docker Compose. También hemos trabajado con redes internas, comunicación entre contenedores, variables de entorno y almacenamiento persistente.



La separación entre frontend, backend y base de datos permite tener una arquitectura más organizada y segura. Además, el uso de volúmenes evita perder la información almacenada cuando detenemos los contenedores.

