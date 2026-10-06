from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_cliente_view, name='registro_cliente'),
    path('mi-perfil/', views.perfil_cliente_view, name='perfil_cliente'),
    
    
    path('panel-admin/', views.panel_admin_view, name='panel_admin'),
    path('empresa/nueva/', views.empresa_crear_view, name='empresa_crear'),
    path('empresa/<int:empresa_id>/empleados/', views.agregar_empleado_view, name='agregar_empleado'),
    path('empresa/<int:empresa_id>/desactivar/', views.desactivar_empresa_view, name='desactivar_empresa'),
    path('repartidor/nuevo/', views.repartidor_crear_view, name='repartidor_crear'),
    path('usuario/<int:perfil_id>/desactivar/', views.desactivar_usuario_view, name='desactivar_usuario'),
    path('admin/nuevo/', views.crear_admin_view, name='crear_admin'),
]