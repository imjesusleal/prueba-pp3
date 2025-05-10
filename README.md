# Pre-setup del ambiente de desarrollo

Lo primero que tienen que instalar es el controlador del driver que vamos a utilizar para acceder a la base de datos.
Como en nuestro caso vamos a usar SqlServer, necesitaremos el ODBC Driver, que es el controlador de Microsoft que usa pyodbc (nuestro driver logico que llamaremos desde python) para poder conectarse a una instancia de un servidor en sql server. Descarguenlo aquí:

[ODBC DRIVER](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)

Otra cosa que utilizo regularmente es Make, y por eso ven en el repositorio un Makefile. Make es una herramienta que originalmente se creo para facilitar el proceso de compilacion y linkeo de ejecutables con sus librerias, pero hoy en dia te sirve para un monton de cosas. Se usa definiendo reglas, que van a ser tu forma de ejecutar comandos en la terminal. Si quieren descargarlo y usarlo, ya les arme algunas reglas en el Makefile:

[Make](https://cmake.org/download/)

## Setup del ambiente de desarrollo

Lo primero que tienen que recordar es aislar su ambiente global, con su ambiente de desarrollo, para eso crearemos un ambiente virtual que sirva para esto. Si no se acuerdan es:

```python
python -m venv aquivaelnombredetuambientevirtual
```

Yo suelo hacer algo sencillo como:
```python
python -m venv .venv
```

Asi mi ambiente virtual es una carpeta oculta, que luego voy a ignorar en mi control de versiones.

Una vez tenga el ambiente virtual acuerdense de activarlo y luego lo unico que necesitan hacer es instalar los paquetes requeridos del proyecto que les deje en el requirements.txt

```python
pip install -r requirements.txt
```

Si no me equivoco asi instalabas todo lo que esta en el archivito de manera recursiva.

## Estructura del proyecto
	├── .venv/
	├── api/
	├── db/
	├── models/       
	├── repository/   
	├── services/     
	├── tests/        

Esta es la estructura basica del proyecto. Les explico a qué se refiere cada carpeta:  
```
.venv -> carpeta de entorno virtual
*api/ -> carpeta donde van a estar los archivos de los routers para capturar las solicitudes HTTP.
*db/ -> carpeta de configuracion de conexión a la base de datos
*models/ -> modelos de nuestras entidades de la base de datos.
repository/ -> carpeta donde estarán nuestro repositorio, sería nuestra carpeta de capa de datos.
services/ -> carpeta donde estan los servicios que usaremos, sería nuestra carpeta de capa de logica de negocio.
tests/ -> carpeta donde van a estar todos los tests.
```

Los que estan marcado con un asterisco (*) son requeridas, las demas son opcionales, pero muy recomendadas. 
Si bien la lógica podemos escribirla toda en los routers, no es una buena practica, y por eso separamos nuestro programa en capas para que se pueda entender y mantener mas fácil.

## Estructura de archivos
Esta por definir, pero me gustaria hacer algo tipo:

```
	├── api/
           ├── unrouter/
                       ├── unrouter.py
           ├── otrorouter/
                       ├── unrouter.py
```

Creo que si seguimos esta dinamica en todos lados, estaremos ok.

## Explicaciones de comandos en el Makefile

Si decidieron descargar Make, harán su proceso de desarrollo y prueba mucho mas sencillo. El Makefile está definido de esta manera por ahora:

```
.PHONY: format
format:
	black .
	isort .
	flake8
	mypy api/ core/ db/ models/ services/ tests/  

.PHONY: dev
dev:
	fastapi dev main.py

.PHONY: test
test:
	pytest

.PHONY: test verbose
test:
	pytest -vs

.PHONY: install
install:
	pip install -r requirements.txt
	pre-commit install

```

Cada ".PHONY" es una regla que pueden utilizar para ejecutar todos los comandos internos definidos por la regla. Por ejemplo, si ejecuto lo siguiente: 

```
make format
```

Se ejecutarán los siguientes comandos en la terminal:

```
	black .
	isort .
	flake8
	mypy api/ core/ db/ models/ services/ tests/  
```

En vez de escribir los comandos uno por uno para su ejecución, los ejecuto de una sola vez. Easy pizi.


## Logica

Esta parte la dejo por si queremos agregar algo. Comiencen viendo como escribi un par de cositas y vayan probando.