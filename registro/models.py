from django.db import models
from django.contrib.auth.models import User
from .validators import validar_rut

class Empresa(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    email = models.EmailField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    saldo_beneficio = models.IntegerField(default=0, help_text="Monto de beneficio (ej: 200000)")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class EmpleadoAutorizado(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='empleados_autorizados')
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, validators=[validar_rut])
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('empresa', 'rut')

    def __str__(self):
        return f"{self.nombre} - {self.rut} ({self.empresa.nombre})"

class PerfilUsuario(models.Model):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('REPARTIDOR', 'Repartidor'),
        ('CLIENTE', 'Cliente'),
    )
    VEHICULOS = (
        ('AUTOMOVIL', 'Automóvil'),
        ('MOTOCICLETA', 'Motocicleta'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES)
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    
    tipo_vehiculo = models.CharField(max_length=20, choices=VEHICULOS, blank=True, null=True)

   
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    tiene_beneficio = models.BooleanField(default=False)
    monto_beneficio = models.IntegerField(default=0)

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol} ({self.rut})"

