El .env.examplo archivo contiene variables de entorno necesarias para la configuración del proyecto. Asegúrate de crear un archivo .env en el mismo directorio que este README.md y de definir las siguientes variables:

```plaintext  
OPENAI_API_KEY=tu_clave_de_api_aqui
```
Reemplaza `tu_clave_de_api_aqui` con tu clave de API real de OpenAI.

# Configuración del Entorno

1. Crea un archivo `.env` en el directorio raíz del proyecto.
2. Copia el contenido del archivo `.env.example` en el nuevo archivo `.env`.
3. Actualiza las variables con tus valores específicos.
4. Guarda el archivo `.env`.
5. Asegúrate de que el archivo `.env` esté incluido en tu archivo `.gitignore` para evitar subirlo a repositorios públicos.
6. Reinicia tu entorno de desarrollo para que los cambios surtan efecto.
# Ejemplo de archivo .env

```plaintext    
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
# Uso de las Variables de Entorno
En tu código, puedes acceder a las variables de entorno utilizando bibliotecas como `dotenv` en Node.js o `os` en Python. Asegúrate de cargar las variables de entorno al inicio de tu aplicación.
Por ejemplo, en Python:

```python
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
print(f"Tu clave de API es: {api_key
}")
```
# Instalar requerimientos
Antes de ejecutar el proyecto, asegúrate de instalar las dependencias necesarias. Puedes hacerlo ejecutando el siguiente comando:

```bash 
pip install -r requirements.txt
```

# Configurar el .venv
Si deseas utilizar un entorno virtual para aislar las dependencias del proyecto, puedes crear y activar un entorno virtual de la siguiente manera:

```bash
# Crear un entorno virtual
python -m venv .venv
# Activar el entorno virtual
# En Windows
.venv\Scripts\activate
```
Para desactivar el entorno virtual, simplemente ejecuta:
```bash 
deactivate
```

# Levantar la aplicación
Para iniciar la aplicación, ejecuta el siguiente comando en tu terminal:
```bash
python main.py
```