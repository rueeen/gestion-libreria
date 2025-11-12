[README.md](https://github.com/user-attachments/files/23504608/README.md)
# 📚 Gestión de Librería

Aplicación web desarrollada con **Django** para la administración de libros, autores, categorías y ventas de una librería.  
El entorno del proyecto se maneja mediante **Pipenv**, lo que garantiza la compatibilidad de dependencias y versiones de Python.

---

## ⚙️ Requisitos previos

Antes de iniciar, asegúrate de tener instalados los siguientes componentes:

- **Python** (versión recomendada: 3.10 o 3.11)  
- **Pipenv** (administrador de entornos virtuales y dependencias)  
- **Git**

> ⚠️ Si el proyecto fue creado con una versión diferente de Python, Pipenv intentará usarla.  
> Puedes verificar o especificar la versión en el archivo `Pipfile`:
> ```toml
> [requires]
> python_version = "3.10"
> ```
> Si tu sistema tiene otra versión (por ejemplo 3.11 o 3.12), modifica esta línea según tu versión instalada.

---

## 🚀 Instalación y ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/rueeen/gestion-libreria.git
cd gestion-libreria
```

---

### 2️⃣ Instalar dependencias con Pipenv

Si no tienes Pipenv, instálalo:

```bash
pip install pipenv
```

Luego crea el entorno virtual e instala las dependencias:

```bash
pipenv install
```

Si tienes más de una versión de Python instalada y el entorno no se crea correctamente, puedes forzar la versión:

```bash
pipenv --python 3.10 install
```

Una vez instalado, activa el entorno virtual:

```bash
pipenv shell
```

---

### 3️⃣ Aplicar migraciones de la base de datos

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4️⃣ Crear un superusuario (opcional)

```bash
python manage.py createsuperuser
```

---

### 5️⃣ Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

Abre en el navegador:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📂 Estructura del proyecto

```
gestion-libreria/
├── catalogo/              # App principal con modelos, vistas y templates
├── gestion_libreria/      # Configuración principal del proyecto Django
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── templates/             # Plantillas HTML
├── db.sqlite3             # Base de datos local (puede regenerarse)
├── Pipfile / Pipfile.lock # Definición del entorno y dependencias Pipenv
└── manage.py              # Archivo principal para ejecutar comandos Django
```

---

## 🧰 Comandos útiles de Pipenv

| Acción | Comando |
|--------|----------|
| Instalar dependencias | `pipenv install` |
| Activar entorno virtual | `pipenv shell` |
| Ejecutar servidor sin activar entorno | `pipenv run python manage.py runserver` |
| Instalar un nuevo paquete | `pipenv install nombre_paquete` |
| Ver dependencias instaladas | `pipenv graph` |
| Salir del entorno virtual | `exit` |

---

## ⚠️ Problemas comunes con entornos

1. **Error de versión de Python no compatible**  
   → Verifica tu versión de Python con `python --version`.  
   Si difiere del `Pipfile`, edítalo o ejecuta:  
   ```bash
   pipenv --python 3.10 install
   ```

2. **El entorno no se activa automáticamente**  
   → Usa `pipenv shell` antes de ejecutar cualquier comando de Django.

3. **Base de datos no sincronizada**  
   → Ejecuta `python manage.py migrate` nuevamente.

---

## 🤝 Colaboración

1. Crea una nueva rama:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
2. Realiza tus cambios y confírmalos:
   ```bash
   git commit -m "Agrega nueva funcionalidad"
   ```
3. Envía tu rama al repositorio:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
4. Crea un Pull Request en GitHub.

---

## 📝 Licencia
Proyecto educativo de código abierto, creado con fines formativos.  
Puedes modificarlo y reutilizarlo libremente con fines académicos.

---

## 👤 Autor

**Ruben Valencia Arancibia**  
[GitHub: rueeen](https://github.com/rueeen)
