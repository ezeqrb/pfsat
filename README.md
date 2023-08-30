# Proyecto Final: Software para llevar a cabo el Seguimiento de Adherencia Terapéutica en pacientes con dislipidemia (PF_SAT)

Para poder ejecutar el software, es necesario crear un entorno virtual que contenga las dependencias del proyecto, presentes en el archivo *requirements.txt*. Para ello, hay que realizar los siguientes pasos:

**Paso 1)** Ubicarse en el directorio raíz del proyecto (*PF_SAT*), abrir una nueva terminal, crear un entorno virtual mediante el siguiente comando  `python -m venv myenv`  y activarlo por medio del comando  `.\myenv\Scripts\Activate`. (Tener en cuenta que estos comandos corresponden a una máquina con sistema operativo Windows).

**Paso 2)**  Ejecutar el comando  `pip install -r requirements.txt`  para instalar todas las dependencias del proyecto.

Además, es necesario definir las variables de entorno utilizadas. Para ello, hay que crear un archivo *.env* donde se declaren las variables de entorno presentes en el archivo *.env.example*.

A partir de entonces, el programa se puede ejecutar utilizando el siguiente comando: `python manage.py runserver`.
