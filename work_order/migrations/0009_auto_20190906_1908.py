# Generated by Django 2.2 on 2019-09-06 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0008_workorder_replay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder_replay',
            name='replay_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='申请时间'),
        ),
    ]