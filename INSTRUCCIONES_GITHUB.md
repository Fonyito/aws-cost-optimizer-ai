# 📦 Instrucciones para Subir el Proyecto a GitHub

## Paso 1: Crear repositorio en GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Haz clic en el botón **"+"** (arriba derecha) → **"New repository"**
3. Configura el repositorio:
   - **Repository name**: `aws-cost-optimizer-ai`
   - **Description**: `🤖 Herramienta de análisis y optimización de costes AWS con IA (Amazon Bedrock + Claude 3.5)`
   - **Visibility**: Public
   - **NO marques** "Initialize this repository with a README" (ya tenemos uno)
4. Haz clic en **"Create repository"**

---

## Paso 2: Inicializar Git local (si no está inicializado)

\`\`\`bash
cd aws-cost-optimizer-ai

# Verificar si ya está inicializado
git status

# Si no está inicializado, ejecutar:
git init
\`\`\`

---

## Paso 3: Añadir archivos al repositorio

\`\`\`bash
# Añadir todos los archivos
git add .

# Verificar qué archivos se añadirán
git status

# Hacer el primer commit
git commit -m "feat: proyecto inicial AWS Cost Optimizer AI con Bedrock"
\`\`\`

---

## Paso 4: Conectar con GitHub y subir

\`\`\`bash
# Añadir el repositorio remoto (reemplaza TU-USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU-USUARIO/aws-cost-optimizer-ai.git

# Verificar que se añadió correctamente
git remote -v

# Cambiar a rama main (si estás en master)
git branch -M main

# Subir el código a GitHub
git push -u origin main
\`\`\`

---

## Paso 5: Verificar en GitHub

1. Ve a tu repositorio: `https://github.com/TU-USUARIO/aws-cost-optimizer-ai`
2. Verifica que todos los archivos estén subidos
3. El README.md debería mostrarse automáticamente en la página principal

---

## Paso 6: Configurar GitHub Pages (opcional)

Para mostrar el dashboard como página web:

1. Ve a tu repositorio en GitHub
2. Clic en **Settings** → **Pages**
3. En "Source", selecciona **"Deploy from a branch"**
4. Branch: **main**, Folder: **/ (root)**
5. Clic en **Save**
6. Espera unos minutos y tu dashboard estará en:
   `https://TU-USUARIO.github.io/aws-cost-optimizer-ai/templates/dashboard.html`

---

## Paso 7: Añadir Topics (etiquetas)

Para mejorar la visibilidad del proyecto:

1. En tu repositorio, haz clic en el ⚙️ junto a "About"
2. Añade estos topics:
   - `aws`
   - `cost-optimization`
   - `finops`
   - `amazon-bedrock`
   - `claude-ai`
   - `serverless`
   - `terraform`
   - `python`
   - `devops`
   - `aws-cost-explorer`

---

## Paso 8: Personalizar README para Malt

Edita el README.md y reemplaza:

- `[Tu Nombre]` → Tu nombre real
- `tu-usuario` → Tu usuario de GitHub
- `tu-perfil` → Tu perfil de Malt
- `tu@email.com` → Tu email de contacto
- `https://www.malt.es/profile/tu-perfil` → Tu URL de Malt

\`\`\`bash
# Después de editar
git add README.md
git commit -m "docs: personalizar README con información de contacto"
git push
\`\`\`

---

## Paso 9: Crear Release (versión)

1. Ve a tu repositorio en GitHub
2. Clic en **"Releases"** (lado derecho)
3. Clic en **"Create a new release"**
4. Tag version: `v1.0.0`
5. Release title: `v1.0.0 - Primera versión`
6. Description:
   \`\`\`
   🎉 Primera versión de AWS Cost Optimizer AI
   
   Características:
   - ✅ Análisis de costes con AWS Cost Explorer
   - ✅ IA con Amazon Bedrock (Claude 3.5)
   - ✅ Dashboard visual interactivo
   - ✅ Modo demo sin AWS
   - ✅ Terraform para despliegue
   - ✅ CI/CD con GitHub Actions
   \`\`\`
7. Clic en **"Publish release"**

---

## Paso 10: Añadir imagen de preview (opcional)

Para que el README se vea más profesional:

1. Genera una captura de pantalla del dashboard
2. Súbela a `docs/dashboard-preview.png`
3. Commit y push:

\`\`\`bash
git add docs/dashboard-preview.png
git commit -m "docs: añadir captura del dashboard"
git push
\`\`\`

---

## 🎯 Comandos Rápidos (resumen)

\`\`\`bash
# Desde el directorio del proyecto
cd aws-cost-optimizer-ai

# Inicializar y subir
git init
git add .
git commit -m "feat: proyecto inicial AWS Cost Optimizer AI"
git remote add origin https://github.com/TU-USUARIO/aws-cost-optimizer-ai.git
git branch -M main
git push -u origin main
\`\`\`

---

## 📝 Actualizaciones Futuras

Para subir cambios futuros:

\`\`\`bash
# Hacer cambios en el código...

# Añadir cambios
git add .

# Commit con mensaje descriptivo
git commit -m "feat: nueva funcionalidad X"

# Subir a GitHub
git push
\`\`\`

---

## 🔗 Enlaces Útiles

- [Guía de Git](https://git-scm.com/book/es/v2)
- [Guía de GitHub](https://docs.github.com/es)
- [Conventional Commits](https://www.conventionalcommits.org/es/)

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Código subido correctamente
- [ ] README personalizado con tu información
- [ ] Topics añadidos al repositorio
- [ ] Release v1.0.0 creada
- [ ] Proyecto probado en modo demo
- [ ] URL del repositorio añadida a tu perfil de Malt

---

¡Listo! Tu proyecto ya está en GitHub y listo para mostrar en Malt 🚀
