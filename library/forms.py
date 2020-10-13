
from .models import Requisition
from django import forms


class RequisitionCreateForm(forms.ModelForm):
    class Meta:
        fields = ('book','user',)
        model = Requisition