# Generated by Django 2.2 on 2019-09-16 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_headportrait'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile_headportrait',
            old_name='headportrait_image',
            new_name='image',
        ),
        migrations.RemoveField(
            model_name='userprofile_headportrait',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='headportrait',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headportrait', to='users.UserProfile_HeadPortrait', verbose_name='头像'),
        ),
    ]
