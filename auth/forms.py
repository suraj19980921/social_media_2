from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class  LoginForm(AuthenticationForm):
    use_required_attribute = False
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'username'}))
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control','id':'password'})



class SingupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email']
        widgets ={
                    'username':forms.TextInput(attrs={'class':'form-control'}),
                    'first_name':forms.TextInput(attrs={'class':'form-control'}),
                    'last_name':forms.TextInput(attrs={'class':'form-control'}),
                    'email':forms.TextInput(attrs={'class':'form-control'})
                 
                 }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None