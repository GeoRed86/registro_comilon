from django import forms
from django.contrib.auth.models import User
from .models import Empresa, EmpleadoAutorizado, PerfilUsuario
from .validators import validar_rut

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class RegistroClienteForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    nombre = forms.CharField(label="Nombre Completo", max_length=150)
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    rut = forms.CharField(label="RUT Personal (12.345.678-9)", validators=[validar_rut])
    telefono = forms.CharField(label="Teléfono", required=False)
    direccion = forms.CharField(label="Dirección", required=False)
    rut_empresa = forms.CharField(
        label="RUT Empresa (Opcional, si cuenta con convenio)",
        required=False,
        validators=[validar_rut]
    )

    def clean_rut(self):
        rut = self.cleaned_data['rut'].upper().strip()
        if PerfilUsuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya se encuentra registrado.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

class RegistroAdminForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    nombre = forms.CharField(label="Nombre Completo", max_length=150)
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    rut = forms.CharField(label="RUT (12.345.678-9)", validators=[validar_rut])

    def clean_rut(self):
        rut = self.cleaned_data['rut'].upper().strip()
        if PerfilUsuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya se encuentra registrado.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

class RegistroRepartidorForm(forms.Form):
    username = forms.CharField(label="Usuario", max_length=150)
    nombre = forms.CharField(label="Nombre Completo", max_length=150)
    email = forms.EmailField(label="Correo")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput)
    rut = forms.CharField(label="RUT (12.345.678-9)", validators=[validar_rut])
    telefono = forms.CharField(label="Teléfono")
    tipo_vehiculo = forms.ChoiceField(
        choices=[('AUTOMOVIL', 'Automóvil'), ('MOTOCICLETA', 'Motocicleta')],
        label="Tipo de Vehículo"
    )

    def clean_rut(self):
        rut = self.cleaned_data['rut'].upper().strip()
        if PerfilUsuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")
        return cleaned_data

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'rut', 'email', 'direccion', 'telefono', 'saldo_beneficio']
        labels = {
            'nombre': 'Nombre Empresa',
            'rut': 'RUT Empresa',
            'email': 'Correo Empresa',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
            'saldo_beneficio': 'Saldo / Monto Beneficio (Ej: 200000)'
        }

   
    def clean_saldo_beneficio(self):
        saldo = self.cleaned_data.get('saldo_beneficio')
        if saldo is not None and saldo < 0:
            raise forms.ValidationError("El saldo de beneficio no puede ser un valor negativo.")
        return saldo

class EmpleadoAutorizadoForm(forms.ModelForm):
    class Meta:
        model = EmpleadoAutorizado
        fields = ['nombre', 'rut']
        labels = {
            'nombre': 'Nombre Empleado',
            'rut': 'RUT Empleado (12.345.678-9)'
        }