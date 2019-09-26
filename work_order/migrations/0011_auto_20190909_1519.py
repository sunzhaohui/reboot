# Generated by Django 2.2 on 2019-09-09 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('work_order', '0010_auto_20190909_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder_replay',
            old_name='replay_contents',
            new_name='reply_contents',
        ),
        migrations.RenameField(
            model_name='workorder_replay',
            old_name='replay_time',
            new_name='reply_time',
        ),
        migrations.RemoveField(
            model_name='workorder_replay',
            name='replayer',
        ),
        migrations.AddField(
            model_name='workorder_replay',
            name='replyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replyer', to=settings.AUTH_USER_MODEL, verbose_name='回复人'),
        ),
    ]
