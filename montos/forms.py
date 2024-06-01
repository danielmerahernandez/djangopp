from django import forms
from montos.models import *

class RegistroGastoForm(forms.ModelForm):
    class Meta:
        model = RegistroGasto
        fields = ['cuenta', 'fecha', 'motivo', 'monto']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del gasto'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto'}),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        cuenta = self.cleaned_data.get('cuenta')

        if cuenta and monto and cuenta.saldo < monto:
            raise forms.ValidationError("Saldo insuficiente en la cuenta.")
        
        return monto

class FechaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Seleccione una fecha')

class RangoFechasForm(forms.Form):
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de inicio')
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de fin')    