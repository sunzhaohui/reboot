# Generated by Django 2.2 on 2019-08-26 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deploy',
            name='review_time',
            field=models.DateTimeField(null=True, verbose_name='处理时间'),
        ),
        migrations.AlterField(
            model_name='deploy',
            name='deploy_time',
            field=models.DateTimeField(null=True, verbose_name='上线完成时间'),
        ),
        migrations.AlterField(
            model_name='deploy',
            name='status',
            field=models.IntegerField(choices=[(0, '申请'), (1, '审核'), (2, '上线'), (3, '取消上线'), (4, '已上线'), (5, '失败')], default=0, verbose_name='上线状态'),
        ),
    ]
