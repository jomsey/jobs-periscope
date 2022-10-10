from django.urls import path,include
from django.conf.urls.static import static
from django.contrib import auth
from django.conf import settings
from . import views


urlpatterns = [
    path("",views.IndexView.as_view(),name='index'),
    path("jobs",views.JobsListView.as_view(),name="jobs_list"),
    path("job_details",views.JobDetailView.as_view(),name="job_details"),
    path("post/<int:pk>",views.PostDetailView.as_view(),name="post_detail"),
    path("profile",views.USerProfileView.as_view(),name="profile"),
    path("auth/login",views.LoginView.as_view(),name="login"),
    path("auth/logout",views.UserLogoutView.as_view(),name="logout"),
    path("auth/create-account",views.UserRegisterView.as_view(),name="register")
] 

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
