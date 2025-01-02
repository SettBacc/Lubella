from django import forms
from .models import WorkingDay

class WorkingDayForm(forms.ModelForm):
    class Meta:
        model = WorkingDay
        fields = ['pallet_id', 'made_pallets']