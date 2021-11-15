from django import forms
from django.db.models import fields
from main import models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].widget = forms.FileInput(attrs={'class':'form-control'})
        
        
class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['image','post']
        widgets = {
                    'post': forms.Textarea(attrs={'class':'form-control', 'cols':'0','rows':'0'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['image'].widget = forms.FileInput(attrs={'class':'form-control'})


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']
        widgets = {
                    'comment': forms.TextInput(attrs={'id':'commentText','class':'form-control'})
        }
    
   
