from django import forms
from core.models import Job, JobApplication, SiteUser


class PostCommentForm(forms.Form):
    comment = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"placeholder":"write a comment","class":"p-4 mt-4"}) )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=SiteUser
        fields=["profile_pic", 'username', 'email','phone_number',  'biography','nationality','birthday']
        widgets = {
            'profile_pic':forms.FileInput(attrs={'placeholder': 'Username','class':"form-control form-control-input" }),
            'username': forms.TextInput(attrs={'placeholder': 'Username','class':"form-control form-control-input" }),
            'email': forms.EmailInput(attrs={'placeholder': 'Email' ,'class':"form-control form-control-input" ,'id':'em'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone number','class':"form-control form-control-input","type":"tel" }),
            'biography': forms.Textarea(attrs={'placeholder': 'Biography','class':"form-control form-control-input",'required':''}),
            'nationality': forms.Select(attrs={'class':"form-select" }),
            'birthday': forms.DateInput(attrs={'class':"form-control form-control-input" }),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model=JobApplication
        fields=['cv',]
        widgets={
                'cv':forms.FileInput(attrs={'class':"form-control form-control-input" }),
 
        }
   
        
class AddNewJobForm(forms.ModelForm):
    class Meta:
        model=Job
        fields=["title","job_type","expiring_date","description","category","years_of_experience"]
        
        widgets = {
            
             'title': forms.TextInput(attrs={'placeholder': 'Title','class':"form-control form-control-input" }),
             'job_type':forms.Select(attrs={'class':'form-select' ,'aria-label':"Default select example" }),
            'expiring_date': forms.SelectDateWidget(attrs={'placeholder': 'Expiry date','class':"form-control form-control-input"}),
             'description': forms.Textarea(attrs={'placeholder': 'Job Description','class':"form-control form-control-input"}),  

        }
