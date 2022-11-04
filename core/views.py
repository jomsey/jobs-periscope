from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import View,DetailView,ListView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from hitcount.views import HitCountDetailView
from core.forms import PostCommentForm, UserProfileForm
from core import models


class IndexView(View):
    template ='pages/index.html'
    def get(self,request):
        latest_posts = models.Post.objects.order_by('-date_created')[:3]
        context={'latest_posts':latest_posts}
        query =  request.GET.get('query')
        if query:
            return HttpResponseRedirect(f'jobs?query={query}')
        return render(request,self.template,context=context)
    
    
class USerProfileView(LoginRequiredMixin,View):
    template="pages/profile.html"
    login_url='/auth/login'
    
    

    def get(self,request):
        user_notifications = models.Notification.objects.filter(user=self.request.user).order_by('-date').select_related('user')
        form =UserProfileForm(instance=self.request.user)
        
        context  = {'form':form,
                    'notifications':user_notifications}
        
        return render(request,self.template,context)
  
    def post(self,request):
        form =UserProfileForm(instance=request.user,data=request.POST)
        if form.is_valid():
            form.save()
        return render(request,self.template,{"form":form})

class JobDetailView(DetailView):
    model=models.Job
    template_name="pages/job-details.html"
    context_object_name = "job"
    
    def get_object(self, queryset=None):
        queryset = self.get_queryset() if queryset is None else queryset
        return get_object_or_404(queryset, title=self.kwargs['title'])
  
    
class JobsListView(ListView):
    model=models.Job
    context_object_name="jobs"
    template_name="pages/jobs.html"
    paginate_by =10
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return models.Job.objects.filter(Q(category__name__startswith=query ) |Q(category__name__icontains=query ) | Q(title__icontains=query ) | Q(job_type__icontains=query ) | Q(title__startswith=query ) | Q(job_type__startswith=query ))
        return models.Job.objects.all().order_by("-date_published")
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_categories']=models.JobCategory.objects.all()
        return context
    
 
class PostsListView(ListView):
    model=models.Post
    context_object_name="posts"
    template_name="pages/posts.html"
    paginate_by =6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_posts"] = models.Post.objects.select_related('user').order_by("views")[:5]
        context["featured_posts"]=models.FeaturedPost.objects.select_related('post').all()[:3]
        return context
    
    
class PostDetailView(HitCountDetailView):
    model =  models.Post
    template_name="pages/detailed_post.html"
    context_object_name = "post"
    count_hit = True
    
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
            return redirect("login")
        return redirect("post_detail",kwargs.get("pk") )
    
class JobApplicationView(View):
    pass


class CreateNewJobView(View):
    pass

