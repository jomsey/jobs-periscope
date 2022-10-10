from django.contrib import admin
from . models import(Job,
                     JobApplication,
                     SiteUser,
                     JobCategory,
                     PostComments,
                     PostLikes,Post)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass

@admin.register(SiteUser)
class SiteUserAdmin(admin.ModelAdmin):
    pass

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(PostComments)
class PostCommentsAdmin(admin.ModelAdmin):
    pass
@admin.register(PostLikes)
class PostLikesAdmin(admin.ModelAdmin):
    pass

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    pass




