from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Empresa, EmpleadoAutorizado, PerfilUsuario
from .forms import (
    LoginForm,
    RegistroClienteForm,
    EmpresaForm,
    EmpleadoAutorizadoForm,
    RegistroRepartidorForm,
    RegistroAdminForm
)

def es_admin(user):
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'perfil') and user.perfil.rol == 'ADMIN'))

def es_superuser(user):
    return user.is_authenticated and user.is_superuser

def login_view(request):
    if request.user.is_authenticated:
        if es_admin(request.user):
            return redirect('panel_admin')
        return redirect('perfil_cliente')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(request, username=u, password=p)
            if user is not None:
                login(request, user)
                if es_admin(user):
                    return redirect('panel_admin')
                return redirect('perfil_cliente')
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_cliente_view(request):
    es_administrador = es_admin(request.user)

    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['nombre']
            )

            rut_cliente = data['rut']
            rut_empresa = data.get('rut_empresa')
            empresa_asociada = None
            tiene_beneficio = False
            monto = 0

           
            if rut_empresa:
                rut_empresa = rut_empresa.upper().strip()
                empresa_qs = Empresa.objects.filter(rut=rut_empresa, activo=True)
                if empresa_qs.exists():
                    empresa_obj = empresa_qs.first()
                    es_empleado = EmpleadoAutorizado.objects.filter(
                        empresa=empresa_obj,
                        rut=rut_cliente,
                        activo=True
                    ).exists()

                    if es_empleado:
                        empresa_asociada = empresa_obj
                        tiene_beneficio = True
                        monto = empresa_obj.saldo_beneficio
                        messages.success(request, f"Cliente con beneficio empresa verificado: ${monto}")
                    else:
                        messages.warning(request, "RUT de empresa ingresado, pero no figura en la nómina autorizada.")
                else:
                    messages.error(request, "El RUT de empresa no corresponde a ninguna empresa activa.")

            PerfilUsuario.objects.create(
                user=user,
                rol='CLIENTE',
                rut=rut_cliente,
                telefono=data.get('telefono'),
                direccion=data.get('direccion'),
                empresa=empresa_asociada,
                tiene_beneficio=tiene_beneficio,
                monto_beneficio=monto
            )
            
            
            if es_administrador:
                messages.success(request, f"Cliente {user.username} registrado exitosamente.")
                return redirect('panel_admin')
            
            return redirect('login')
    else:
        form = RegistroClienteForm()
        
    return render(request, 'registro_cliente.html', {
        'form': form,
        'desde_admin': es_administrador
    })

@login_required
def perfil_cliente_view(request):
    perfil = getattr(request.user, 'perfil', None)
    return render(request, 'perfil_cliente.html', {'perfil': perfil})



@user_passes_test(es_superuser)
def crear_admin_view(request):
    if request.method == 'POST':
        form = RegistroAdminForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['nombre'],
                is_staff=True  
            )
            PerfilUsuario.objects.create(
                user=user,
                rol='ADMIN',
                rut=data['rut']
            )
            messages.success(request, f"Administrador {user.username} creado con éxito.")
            return redirect('panel_admin')
    else:
        form = RegistroAdminForm()
    return render(request, 'formulario_admin.html', {'form': form})



@user_passes_test(es_admin)
def panel_admin_view(request):
    empresas = Empresa.objects.filter(activo=True)
    usuarios = PerfilUsuario.objects.filter(activo=True).select_related('user', 'empresa')
    return render(request, 'panel_admin.html', {
        'empresas': empresas,
        'usuarios': usuarios,
        'es_super': request.user.is_superuser
    })

@user_passes_test(es_admin)
def empresa_crear_view(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa guardada con éxito.")
            return redirect('panel_admin')
    else:
        form = EmpresaForm()
    return render(request, 'formulario_empresa.html', {'form': form})

@user_passes_test(es_admin)
def agregar_empleado_view(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, activo=True)
    empleados = empresa.empleados_autorizados.filter(activo=True)

    if request.method == 'POST':
        form = EmpleadoAutorizadoForm(request.POST)
        if form.is_valid():
            nuevo_emp = form.save(commit=False)
            nuevo_emp.empresa = empresa
            nuevo_emp.rut = nuevo_emp.rut.upper().strip()
            nuevo_emp.save()
            messages.success(request, f"Empleado {nuevo_emp.nombre} añadido a la nómina de {empresa.nombre}.")
            return redirect('agregar_empleado', empresa_id=empresa.id)
    else:
        form = EmpleadoAutorizadoForm()

    return render(request, 'formulario_empleado.html', {
        'empresa': empresa,
        'empleados': empleados,
        'form': form
    })

@user_passes_test(es_admin)
def repartidor_crear_view(request):
    if request.method == 'POST':
        form = RegistroRepartidorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password'],
                first_name=data['nombre']
            )
            PerfilUsuario.objects.create(
                user=user,
                rol='REPARTIDOR',
                rut=data['rut'],
                telefono=data['telefono'],
                tipo_vehiculo=data['tipo_vehiculo']
            )
            messages.success(request, "Repartidor registrado correctamente.")
            return redirect('panel_admin')
    else:
        form = RegistroRepartidorForm()
    return render(request, 'formulario_repartidor.html', {'form': form})

@user_passes_test(es_admin)
def desactivar_usuario_view(request, perfil_id):
    perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
    perfil.activo = False
    perfil.user.is_active = False
    perfil.save()
    perfil.user.save()
    messages.info(request, f"Usuario {perfil.user.username} desactivado (persistencia intacta).")
    return redirect('panel_admin')

@user_passes_test(es_admin)
def desactivar_empresa_view(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.activo = False
    empresa.save()
    messages.info(request, f"Empresa {empresa.nombre} desactivada.")
    return redirect('panel_admin')

    