from django import forms


class PostCommentForm(forms.Form):
    comment = forms.CharField(max_length=500,widget=forms.Textarea(attrs={"placeholder":"write a comment","class":"p-4 mt-4"}) )
   