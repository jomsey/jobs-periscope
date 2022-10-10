# Generated by Django 4.0.6 on 2022-10-09 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_jobcategory_post_alter_siteuser_gender_postlikes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomments',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='biography',
            field=models.TextField(default='Hello world'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='postlikes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
