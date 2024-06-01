from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.shortcuts import redirect, render, get_object_or_404
from datetime import datetime
from django.http import HttpResponseRedirect
from montos.models import *
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from montos.forms import *
from django.db.models import Sum
from datetime import datetime, timedelta
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create your views here.
#------------------------Cuenta-----------------------------------#
def index(request):
    cuentas = Cuenta.objects.all()
    gastos = RegistroGasto.objects.all()

    fecha_form = FechaForm()
    rango_fechas_form = RangoFechasForm()
    total = 0

    if request.method == 'POST':
        if 'buscar_por_fecha' in request.POST:
            fecha_form = FechaForm(request.POST)
            if fecha_form.is_valid():
                fecha = fecha_form.cleaned_data['fecha']
                gastos = RegistroGasto.objects.filter(fecha=fecha)
                total = gastos.aggregate(total=Sum('monto'))['total'] or 0
        elif 'buscar_por_rango' in request.POST:
            rango_fechas_form = RangoFechasForm(request.POST)
            if rango_fechas_form.is_valid():
                fecha_inicio = rango_fechas_form.cleaned_data['fecha_inicio']
                fecha_fin = rango_fechas_form.cleaned_data['fecha_fin']
                gastos = RegistroGasto.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                total = gastos.aggregate(total=Sum('monto'))['total'] or 0
        elif 'generar_pdf' in request.POST:
            fecha = request.POST.get('fecha')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            url = reverse('montos:generar_reporte_pdf')
            if fecha:
                url += f'?fecha={fecha}'
            elif fecha_inicio and fecha_fin:
                url += f'?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}'
            return redirect(url)

    context = {
        'cuentas': cuentas,
        'gastos': gastos,
        'fecha_form': fecha_form,
        'rango_fechas_form': rango_fechas_form,
        'total': total,
    }

    return render(request, 'home.html', context)


def generar_reporte_pdf(request):
    fecha = request.GET.get('fecha')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha:
        gastos = RegistroGasto.objects.filter(fecha=fecha)
        fecha_text = f"Fecha: {fecha}"
        fecha_str = fecha  # String para el nombre del archivo
    elif fecha_inicio and fecha_fin:
        gastos = RegistroGasto.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        fecha_text = f"Desde: {fecha_inicio} Hasta: {fecha_fin}"
        fecha_str = f"{fecha_inicio}_to_{fecha_fin}"  # String para el nombre del archivo
    else:
        gastos = RegistroGasto.objects.all()
        fecha_text = "Todos los registros"
        fecha_str = datetime.now().strftime("%Y-%m-%d")  # Fecha actual para el nombre del archivo

    total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_gastos_{fecha_str}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Reporte de Gastos")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 70, fecha_text)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, height - 100, "Cuenta")
    p.drawString(150, height - 100, "Fecha")
    p.drawString(250, height - 100, "Motivo")
    p.drawString(450, height - 100, "Monto")

    p.setFont("Helvetica", 10)
    y = height - 120
    for gasto in gastos:
        p.drawString(50, y, gasto.cuenta.nombre)
        p.drawString(150, y, str(gasto.fecha))
        p.drawString(250, y, gasto.motivo)
        p.drawString(450, y, str(gasto.monto))
        y -= 20

    y -= 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, f"Total de Gastos: ${total_gastos}")

    p.showPage()
    p.save()
    return response

class CuentaListView(ListView):
    model = Cuenta
class CuentaCreateView(SuccessMessageMixin,CreateView):
    model = Cuenta
    form = Cuenta
    fields = '__all__'
    success_message = "cuenta agregada correctamente"

    def get_success_url(self):
        return reverse('montos:listarcuenta')

class CuentaDetailView(DeleteView):
    model=Cuenta

class CuentaUpdateView(SuccessMessageMixin,UpdateView):
    model = Cuenta
    form = Cuenta
    fields = "__all__"
    success_message = "la cuenta ha sido actualizada correctamente"

    def get_success_url(self):
        return reverse('montos:listarcuenta')
    
class CuentaDeleteView(SuccessMessageMixin,DeleteView):
    model = Cuenta
    form = Cuenta
    fields = "__all__"
    success_message = "la cuenta ha sido eliminada correctamente"

    def get_success_url(self):
        return reverse('montos:listarcuenta')
#------------------------Cuenta-----------------------------------#

#------------------------registro gastos--------------------------#
class RegistroGastoListView(ListView):
    model = RegistroGasto

class RegistroGastoCreateView(SuccessMessageMixin,CreateView):
    model = RegistroGasto
    form_class = RegistroGastoForm
    success_message = "tu gasto ha sido agregado correctamente"

    def form_invalid(self, form):
        # Puedes agregar un mensaje flash si lo deseas
        # messages.error(self.request, "Error al registrar el gasto. Verifica los datos.")
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('montos:listarGasto')
    

class RegistroGastoDetailView(DeleteView):
    model=RegistroGasto

class RegistroGastoUpdateView(SuccessMessageMixin,UpdateView):
    model = RegistroGasto
    form = RegistroGasto
    fields = "__all__"
    success_message = "tu gasto ha sido actualizado correctamente"

    def form_valid(self, form):
        # Obtener la justificación del formulario
        justificacion = form.cleaned_data['justificacion']

        # Guardar el objeto form antes de actualizar el modelo para poder acceder a sus datos
        self.object = form.save(commit=False)

        # Actualizar el modelo con los datos del formulario
        self.object.save()

        # Guardar la justificación en un campo del modelo
        self.object.justificacion = justificacion
        self.object.save()

        # Redireccionar a la URL de éxito
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('montos:listarGasto')
    
class RegistroGastoDeleteView(SuccessMessageMixin,DeleteView):
    model = RegistroGasto
    form = RegistroGasto
    fields = "__all__"
    success_message = "tu gasto ha sido eliminado correctamente"
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        agregar_saldo = request.POST.get('agregar_saldo', 'no') == 'si'
        cuenta = self.object.cuenta

        if agregar_saldo:
            cuenta.saldo += self.object.monto
            cuenta.save()

        self.object.delete()
        messages.success(self.request, self.success_message)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('montos:listarGasto')
#--------------------------------------------------#



