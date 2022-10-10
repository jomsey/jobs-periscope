from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path("",views.IndexView.as_view(),name='index'),
    path("jobs",views.JobsListView.as_view(),name="jobs_list"),
    path("job_details",views.JobDetailView.as_view(),name="job_details"),
    path("post/<int:pk>",views.PostDetailView.as_view(),name="post_detail"),
    path("profile",views.USerDetailView.as_view(),name="profile"),
    path("login",views.LoginView.as_view(),name="login"),
] 

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
