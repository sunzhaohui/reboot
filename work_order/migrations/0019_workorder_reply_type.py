# Generated by Django 2.2 on 2019-09-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0018_auto_20190912_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder_reply',
            name='type',
            field=models.IntegerField(choices=[(0, 'text'), (1, 'markdown')], default=0, verbose_name='回复类型'),
        ),
    ]
