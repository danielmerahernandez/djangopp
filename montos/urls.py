from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from montos.views import *


urlpatterns = [
  path('inicio/', login_required(index), name='index'),
  path('generar_reporte_pdf/', login_required(generar_reporte_pdf), name='generar_reporte_pdf'),
  
 #-----------------------------------------------------------------#
  path('cuenta/', login_required(CuentaListView.as_view(template_name="cuenta/index.html")), name="listarcuenta"),
  path('cuenta/crear', login_required(CuentaCreateView.as_view(template_name="cuenta/crear.html")), name="crearcuenta"),
  path('cuenta/actualizar/<int:pk>', login_required(CuentaUpdateView.as_view(template_name="cuenta/crear.html")), name="editarcuenta"),
  path('cuenta/eliminar/<int:pk>', login_required(CuentaDeleteView.as_view(template_name="cuenta/eliminar.html.html")), name="eliminarcuenta"),
  #----------------------------------------------------------------------------------------------------#
  path('Gasto/', login_required(RegistroGastoListView.as_view(template_name="gasto/index.html")), name="listarGasto"),
  path('Gasto/crear', login_required(RegistroGastoCreateView.as_view(template_name="gasto/crear.html")), name="crearGasto"),
  path('Gasto/editar/<int:pk>', login_required(RegistroGastoUpdateView.as_view(template_name="gasto/crear.html")), name="editarGasto"),
  path('Gasto/eliminar/<int:pk>', login_required(RegistroGastoDeleteView.as_view(template_name="gasto/index.html")), name="eliminarGasto"),
   #----------------------------------------------------------------------------------------------------#
]
