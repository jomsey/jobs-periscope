from django import forms

from core.models import SiteUser


class PostCommentForm(forms.Form):
    comment = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"placeholder":"write a comment","class":"p-4 mt-4"}) )

class UserRegisterForm(forms.ModelForm):
    password2=forms.CharField(max_length=10000,widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password' ,'class':"mt-2 form-control form-control-input"}))
    class Meta:
        model=SiteUser
        fields=["username","email","password","password2"]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username','class':"form-control form-control-input" }),
            'email': forms.EmailInput(attrs={'placeholder': 'Email' ,'class':"form-control form-control-input mt-2 mb-2"}),
            'password':forms.PasswordInput(attrs={'placeholder': 'Password' ,'class':"form-control form-control-input"})
        }
