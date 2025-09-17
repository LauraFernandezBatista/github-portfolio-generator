# GitHub Portfolio Generator (Python)

Genera un `README.md` bonito para tu repositorio usando la **API de GitHub** y una plantilla **Jinja2**.

> Ideal para el *repo de perfil* (`<tu-usuario>/<tu-usuario>`) o para cualquier repo del portfolio.

## 🚀 Características
- Recupera tu **perfil**, **repositorios**, lenguajes principales, repos con más ⭐ y repos **actualizados recientemente**.
- Renderiza un **README.md** con Jinja2.
- **GitHub Actions** diario para mantenerlo actualizado.
- Configurable por **variables de entorno** o parámetro `--username`.

## 🧰 Requisitos
- Python 3.10+
- Cuenta de GitHub

## 🛠️ Uso local
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

pip install -r requirements.txt

# Configura usuario y token (opcional)
cp .env.example .env
# edita .env -> GITHUB_USERNAME=tuUsuario

# Genera README
python generator.py
# o: python generator.py --username tuUsuario
```

El archivo **README.md** se genera en la misma carpeta del script.

## 🤖 GitHub Actions
1. Crea (o usa) un repo: por ejemplo, tu *repo de perfil* `tuUsuario/tuUsuario`.
2. Copia estos archivos a la **raíz** del repo: `generator.py`, `requirements.txt`, `template.md.j2`, `.github/workflows/update-readme.yml`.
3. Haz push. El workflow se ejecutará **cada día** y cuando lo dispares manualmente.

> El workflow usa el `GITHUB_TOKEN` automático del runner — no necesitas crear un token personal para el CI.

## ⚙️ Variables de entorno
- `GITHUB_USERNAME` (obligatorio si no pasas `--username`)
- `GITHUB_TOKEN` (opcional; recomendable para evitar *rate limits* al ejecutar en local).

## 📝 Personaliza tu README
- Cambia la **plantilla** en `template.md.j2` (texto, secciones, emojis).
- Cambia el `tagline` en `generator.py`.

## 📂 Estructura
```
.
├─ generator.py
├─ requirements.txt
├─ template.md.j2
├─ .env.example
├─ .github/
│  └─ workflows/
│     └─ update-readme.yml
└─ PROJECT_README.md
```
