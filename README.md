# ChatBotUPN

Aplicación de Chat Bot para la universidad

## Configuración

```S
# Crear entorno virtual en MAC
python3 -m venv .venv
source .venv/bin/activate

# Crear entorno virtual en Windows
python -m venv .venv
.venv\Scripts\activate

# Instalar los paquetes
pip install -r requirements.txt

# Ejecutar proyecto
gunicorn app:app

# Instalar TailwindCss
npm init -y
npm i -D tailwindcss
npx tailwindcss init
# realizamos las configuraciones indicada en la documentación de TailwindCss
# se crea una archivo en esta ruta ./static/src/tailwind.css para agregar las directivas
# Después de hacer las configuraciones de la documentación, agregamos el ultimo comando
# Ejecutar TailwindCss
npx tailwindcss -i ./static/src/tailwind.css -o ./static/css/main.css --watch

# Ejecutar el proyecto
flask run --debug
```

## Formularios - templates

- Base.html
  - Html principal, que contendrá los estilos y scripts de todo la aplicación.
- Index.html
  - Cuerpo de toda la aplicación, contiende el envío del mensaje y las respuestas.

## Static

- Contiene todas las imágenes, scripts y estilos.
