from django import forms
from .models import WorkingDay

# Formularz do funkcji add_working_day w views.py
class WorkingDayForm(forms.ModelForm):
    class Meta:
        model = WorkingDay  # Powiązanie formularza z modelem WorkingDay
        fields = ['pallet_id', 'made_pallets']  # Pola modelu uwzględnione w formularzu