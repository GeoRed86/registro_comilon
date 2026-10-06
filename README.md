# 🍽️ Sistema de Registro y Convenios para Restaurante

Sistema web desarrollado con **Django** y **SQLite** para la gestión de usuarios, convenios corporativos de alimentación y control de beneficios en un restaurante.

---

## 🚀 Características Principales

- **Gestión Jerárquica de Roles**:
  - **Superusuario**: Control total del sistema y rol exclusivo habilitado para crear Administradores.
  - **Administrador**: Gestión y registro de empresas, repartidores y clientes.
  - **Cliente / Cliente Empresa**: Registro autónomo con cotejo de convenios corporativos.
  - **Repartidor**: Registro con categorización de vehículo (Automóvil / Motocicleta).
- **Validación Automática de Beneficios Corporativos**:
  - Al registrar una empresa se define un saldo asignado para el beneficio (no negativo).
  - La empresa gestiona una nómina autorizada de empleados (Nombre y RUT).
  - Al registrarse un cliente ingresando un RUT de empresa, el sistema coteja automáticamente si pertenece a la nómina activa para asignarle el saldo correspondiente.
- **Validación Estricta de RUT Chileno**:
  - Expresión regular que asegura el formato con puntos, guion y dígito verificador (`12.345.678-9` o `12.345.678-K`).
- **Persistencia de Datos (Soft Delete)**:
  - Los usuarios y empresas no se eliminan físicamente de la base de datos; pasan a estado inactivo (`activo = False`) para mantener la trazabilidad.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python / Django
- **Base de Datos**: SQLite3
- **Frontend**: HTML plano con sistema de mensajes y formularios Django
- **Control de Versiones**: Git & GitHub

---

## 📂 Estructura del Proyecto

```text
registro_comilon/
│
├── config/              # Configuración global del proyecto Django (settings, urls, wsgi)
├── registro/            # Aplicación principal
│   ├── models.py        # Modelos (Empresa, EmpleadoAutorizado, PerfilUsuario)
│   ├── forms.py         # Formularios y validaciones de contraseña/RUT/saldo
│   ├── views.py         # Lógica de registro, login, cotejo y panel admin
│   ├── validators.py    # Validador de formato de RUT
│   └── urls.py          # Enrutamiento de la app
├── templates/           # Plantillas HTML
│   ├── login.html
│   ├── registro_cliente.html
│   ├── perfil_cliente.html
│   ├── panel_admin.html
│   ├── formulario_admin.html
│   ├── formulario_empresa.html
│   ├── formulario_empleado.html
│   └── formulario_repartidor.html
├── manage.py
├── requirements.txt
└── .gitignore