from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class SiteUser(AbstractUser):
    GENDER_CHOICES = (("M","Male"),("F","Female"))
    phone_number = models.CharField(max_length=15)
    birthday = models.DateField(null=True)
    nationality = models.CharField(max_length=15)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    profile_pic = models.ImageField(upload_to="profile_pics",default="avatar.jpg")
    biography = models.TextField()
    
    def __str__(self):
        return self.username
    
    class Meta:
        swappable = "AUTH_USER_MODEL"  
        
          
class JobCategory(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "job_categories"

class Post(models.Model):
    cover_image = models.ImageField(upload_to="post_covers")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now=True)
    post =models.TextField()
    
    def __str__(self) :
        return f'{self.title[:25]} ...'
    
    
class  PostComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    comment = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)
    
class PostLikes(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    
class Job(models.Model):
    title = models.CharField(max_length=200)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    date_published = models.DateTimeField(auto_now_add=True)
    expiring_date = models.DateField()
    description = models.TextField()
    category = models.ForeignKey(JobCategory,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.title
    
    
class JobApplication(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_submitted= models.DateTimeField(auto_now_add=True)
    cv = models.FileField(upload_to="cvs")
    
    def __str__(self):
        return self.job.title