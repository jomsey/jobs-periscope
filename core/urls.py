from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path("",views.IndexView.as_view(),name='index'),
    path("jobs",views.JobsListView.as_view(),name="jobs_list"),
    path("jobs/<str:title>",views.JobDetailView.as_view(),name="job_details"),
    path("blog/post/<int:pk>",views.PostDetailView.as_view(),name="post_detail"),
    path("blog/posts",views.PostsListView.as_view(),name="posts_list"),
    path("profile",views.USerProfileView.as_view(),name="profile"),
    path('auth/', include('allauth.urls')),
] 

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
