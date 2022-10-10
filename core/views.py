from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import View,DetailView,ListView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from core.form import PostCommentForm, UserRegisterForm
from core import models

class IndexView(View):
    def get(self,request):
        latest_posts = models.Post.objects.order_by('-date_created')[:3]
        context={'latest_posts':latest_posts}
        template ='pages/index.html'
        return render(request,template,context=context)
    
    def post(self,request):
        return HttpResponse("OK")


class USerProfileView(LoginRequiredMixin,DetailView):
    login_url='/auth/login'
    def get(self,request):
        return HttpResponse("User Detail")
   

class JobDetailView(DetailView):
    def get(self,request):
        return HttpResponse("Job Detail")

class JobsListView(ListView):
    def get(self,request):
        return HttpResponse("Jobs List")
class PostsListView(ListView):
    pass

class PostDetailView(DetailView):
    model =  models.Post
    template_name="pages/detailed_post.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = models.PostComments.objects.filter(post=kwargs.get("object")).order_by("-date_created")
        context["form"] = PostCommentForm()
        return context
    
    def post(self,request,*args, **kwargs):
        comment_form = PostCommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.cleaned_data.get("comment")
            post = models.Post.objects.filter(id =kwargs.get("pk")).first()
            user = models.SiteUser.objects.filter(id=request.user.id).first()
            
            if  self.request.user.is_authenticated:
                 new_comment = models.PostComments(user=user,comment=comment,post=post)
                 new_comment.save()
                 messages.success(request,"success")
            messages.info(request,"please sign in to comment")
        return redirect("post_detail",kwargs.get("pk") )
    
    
class LoginView(View):
    def get(self,request):
        if request.user.is_authenticated:
             return redirect('profile')
        return render(request,"pages/login.html")
    
    def post(self,request):
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(password=password,username=username)
        if user:
            login(request,user)
            return redirect('profile')
        return render(request,"pages/login.html")
    
class UserRegisterView(View):
    def get(self,request):
        if request.user.is_authenticated:
             return redirect('profile')
        return render(request,"pages/register.html",context={"form":UserRegisterForm})
    
    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
           username = form.cleaned_data.get("username")
           email =form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           password2 = form.cleaned_data.get("password2")
           
           if password == password2:
               new_user = models.SiteUser.objects.create(username=username,password=password,email=email)
               new_user.save()
               login(request,authenticate(username=username,password=password))
               return redirect('profile')
        
        return render(request,"pages/register.html",context={"form":form})
    
class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponse("Ok")
        
        

   
