# Sistema de Denuncias Vecinales

Este proyecto es una plataforma web desarrollada en Django para la gestión y reporte de incidentes ciudadanos (infraestructura, urgencias, observaciones).

## Tecnologías utilizadas
- **Framework:** Django (Python)
- **Base de datos:** PostgreSQL
- **Contenedores:** Docker y Docker Compose
- **Estilos:** CSS personalizado

## Características principales y módulos desarrollados
- **Sistema de Autenticación:** 
  - Registro de usuarios validando mayoría de edad (+18) y DNI único.
  - Inicio de sesión (`login`) seguro mediante credenciales de usuario.
  - Recuperación de contraseña por correo electrónico utilizando las vistas integradas de Django.
  - Cierre de sesión (`logout`).
- **Tablero Público:** 
  - Visualización cronológica de todas las denuncias enviadas por la comunidad.
  - Filtros interactivos por categorías (*Urgentes, Infraestructura, Observaciones*).
- **Gestión de Reportes con Permisos:**
  - Creación de nuevas denuncias con soporte para adjuntar imágenes.
  - **Permisos por usuario:** Funcionalidad de editar y eliminar reportes restringida exclusivamente al autor original de la nota mediante validación de sesión (`@login_required` y verificación de propietario).

## Cómo ejecutar el proyecto
1. Clonar el repositorio.
2. Levantar el entorno con Docker: 
   ```bash
   docker-compose up --build
