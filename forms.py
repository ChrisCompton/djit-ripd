from django.forms import ModelForm
from .models import Item  # Adjust the import path according to your project structure

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'classification']