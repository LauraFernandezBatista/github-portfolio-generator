# GitHub Portfolio Generator

Herramienta en **Python** que genera automáticamente un README de portfolio para GitHub utilizando la API pública de GitHub.

El script obtiene información del perfil (repositorios, estadísticas y actividad reciente) y genera un `README.md` dinámico a partir de una plantilla **Jinja2**.

Esto permite crear o actualizar un README de perfil sin tener que escribirlo manualmente.

---

# Tecnologías

* Python
* GitHub API
* Requests
* Jinja2

---

# Instalación

Clona el repositorio:

```
git clone https://github.com/LauraFernandezBatista/github-portfolio-generator.git
```

Entra en la carpeta del proyecto:

```
cd github-portfolio-generator
```

Instala las dependencias:

```
pip install -r requirements.txt
```

---

# Uso

Ejecuta el script indicando tu usuario de GitHub:

```
python generator.py --username TU_USUARIO_GITHUB
```

Ejemplo:

```
python generator.py --username LauraFernandezBatista
```

El script generará automáticamente el archivo `README.md` con la información del perfil.

---

# Nota importante

⚠️ Cada vez que se ejecuta el script, el archivo `README.md` se **sobrescribe** con el contenido generado a partir de la plantilla.

Si deseas conservar una versión anterior, guarda una copia antes de ejecutar el script nuevamente.

---

# Estructura del proyecto

```
.
├── generator.py
├── template.md.j2
├── requirements.txt
└── .github/workflows
```

---

# Posibles mejoras

* Añadir más estadísticas del perfil
* Permitir seleccionar repositorios destacados
* Generar gráficos de actividad
* Añadir personalización de la plantilla

