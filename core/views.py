from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.views.generic import View,DetailView,ListView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from hitcount.views import HitCountDetailView
from core.forms import PostCommentForm, UserProfileForm,AddNewJobForm,JobApplicationForm
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
        jobs_posted_by_user = models.Job.objects.filter(posted_by=request.user).order_by('-date_published').select_related('posted_by')
        user = get_object_or_404(models.SiteUser,id=request.user.id)
        user_notifications = user.notification_set.all()
        form =UserProfileForm(instance=request.user)
        
        context  = {'form':form,
                    'notifications':user_notifications,
                    'jobs_posted':jobs_posted_by_user,
                     'add_job_form': AddNewJobForm()
                   }
        
        return render(request,self.template,context)
    
    def post(self,request):
        form =UserProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,"Your profile has been edited successfully")
        else:
            messages.error(request,"OOps! Check your from data and try again")
            
        context = {"form":form}
        return HttpResponseRedirect("profile")

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
        context['add_job_form'] = AddNewJobForm()
        return context
    
    def post(self,request):
        form = AddNewJobForm(request.POST);
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request,"Your job has been added successfully")
        else:
            messages.error(request,"OOps! Check your from data and try again")
        return HttpResponseRedirect('jobs')
    
 
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
        context["popular_posts"] = models.Post.objects.select_related('user').order_by("views")[:5]
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
            else:
                messages.info(request,"Cannot submit comment if not logged in !")
        return redirect("post_detail",kwargs.get("pk") )
    

class DeleteJobView(LoginRequiredMixin,View):
    login_url = "/auth/login"
    def get(self,request,id):
        job = get_object_or_404(models.Job,id=id)
        job.delete()
        messages.success(request,"Job has been deleted")
        return redirect("profile")
    
class AddJobView(LoginRequiredMixin,View):
    login_url = "/auth/login"
    
    def post(self,request):
        form = AddNewJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            messages.success(request,"Your job has been added successfully")
        else:
            messages.error(request,"OOps! Check your from data and try again")
        return redirect("profile")
    
    
class JobApplicationView(LoginRequiredMixin,View):
    login_url = "/auth/login"
    def get(self,request,job_id):
        form = JobApplicationForm(request.POST)
        applied_job = get_object_or_404(models.Job,id=job_id)
        return render(request,"pages/application.html",{"form":form,"job":applied_job})
    
    def post(self,request,job_id):
        form = JobApplicationForm(request.POST,request.FILES)
        applied_job = get_object_or_404(models.Job,id=job_id)
       
        print(form.is_valid())
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.jobs=applied_job
            application.save()
            
            messages.success(request,"Your application has been submitted")
            
            #notify the person who posted the job for any applications made
            notification = models.Notification.objects.create()
            job_owner = get_object_or_404(models.SiteUser,id=applied_job.posted_by_id)
            notification.users.set([job_owner])
            notification.information=f"Someone has submitted an application for {applied_job.title}"
            notification.save()
            
        else:
            messages.error (request,"Please check your form data and try again")
        return render(request,"pages/application.html",{"form":form,"job":applied_job})
    
    
class RemoveNotificationView(LoginRequiredMixin,View):
    login_url = "/auth/login"
    
    def get(self,request,notification_id):
        notification = get_object_or_404(models.Notification,id=notification_id)
        print(notification)
        #just remove user from the list of people who were notified
        #cannot delete the notification 'coz could be shared by multiple users
        notification.users.remove(request.user)
        notification.save()
        return redirect("profile")
        