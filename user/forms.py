from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import *
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # widget = {
        #     'is_staff': CheckboxInput()
        # }
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            print(field)
            field.widget.attrs.update({'class':'form-control'})
            field.help_text = ''
        self.fields['username'].widget.attrs.update({'placeholder':'Kullanıcı adını giriniz'})