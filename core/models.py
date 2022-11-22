from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings
from hitcount.models import  HitCount
from django.contrib.contenttypes.fields import GenericRelation
from core.validators import cv_validator
from django_countries.fields import CountryField

class SiteUser(AbstractUser):
    GENDER_CHOICES = (("M","Male"),("F","Female"))
    phone_number = models.CharField(max_length=15,null=True)
    birthday = models.DateField(null=True)
    nationality = CountryField(blank_label='(select country)')
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True)
    profile_pic = models.ImageField(upload_to="profile_pics",default="avatar.jpg")
    biography = models.TextField()
    
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.profile_pic.path)
        if img:
            if img.height > 200 or img.width > 200:
                new_img = (200, 100)
                img.thumbnail(new_img)
                img.save(self.profile_pic.path)
        
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
    views = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    
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


class FeaturedPost(models.Model):
      post = models.ForeignKey(Post,on_delete=models.CASCADE)
      
      def __str__(self):
          return self.post.title
    
    
class Job(models.Model):
    JOB_TYPES = [('Full Time','Full Time'),
                 ('Part Time','Part Time'),
                 ('Remote','Remote')]
    title = models.CharField(max_length=200)
    job_location = models.CharField(max_length=200)
    years_of_experience = models.PositiveIntegerField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    date_published = models.DateTimeField(auto_now_add=True)
    job_type = models.CharField(max_length=20,choices=JOB_TYPES)
    expiring_date = models.DateField()
    description = models.TextField()
    category = models.ForeignKey(JobCategory,on_delete=models.SET_NULL,null=True,related_name='jobs')
    
    
    def __str__(self):
        return self.title
    
    def is_expired(self):
        return date.today()>self.expiring_date
    
    class Meta:
        ordering = ['id']
    
class JobApplication(models.Model):
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_submitted= models.DateTimeField(auto_now_add=True)
    jobs = models.ForeignKey(Job,on_delete=models.CASCADE)
    cv = models.FileField(upload_to="cvs",validators=[cv_validator])
    def __str__(self):
        return self.jobs.title


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date= models.DateTimeField(auto_now_add=True)
    information = models.TextField()
    