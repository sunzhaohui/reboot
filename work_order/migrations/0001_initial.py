# Generated by Django 2.2 on 2019-08-18 08:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='工单标题')),
                ('order_contents', models.TextField(verbose_name='工单内容')),
                ('orderfiles', models.FileField(blank=True, null=True, upload_to='orderfiles/%Y/%m', verbose_name='工单附件')),
                ('status', models.IntegerField(choices=[(0, '申请'), (1, '处理中'), (2, '完成'), (3, '失败')], default=0, verbose_name='工单状态')),
                ('result_desc', models.TextField(blank=True, null=True, verbose_name='处理结果')),
                ('apply_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('complete_time', models.DateTimeField(auto_now=True, verbose_name='处理完成时间')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workorder_applicant', to=settings.AUTH_USER_MODEL, verbose_name='申请人')),
                ('assign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workorder_assign', to=settings.AUTH_USER_MODEL, verbose_name='指派人')),
                ('handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workorder_handler', to=settings.AUTH_USER_MODEL, verbose_name='最终处理人')),
            ],
            options={
                'verbose_name': 'workorder',
                'verbose_name_plural': 'workorder',
                'ordering': ['-complete_time'],
            },
        ),
    ]
