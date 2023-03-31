from django.forms import ModelForm
from .models import *
from django.forms import *
class UrunForm(ModelForm):
    class Meta:
        model = Urun
        fields = ['isim', 'kategori', 'sub_category', 'tek', 'aciklama', 'resim', 'fiyat']
        widgets = {
            'sub_category': CheckboxSelectMultiple()
        }
    def __init__(self, *args, **kwargs):
        super(UrunForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class':'form-control'
            })
        self.fields['sub_category'].widget.attrs.update({'class':''})