# Generated by Django 2.2 on 2019-09-12 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_order', '0017_auto_20190912_1640'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workorder_file',
            name='filesize',
        ),
        migrations.AddField(
            model_name='workorder_file',
            name='fileowner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_owner', to=settings.AUTH_USER_MODEL, verbose_name='上传人'),
        ),
    ]
