# Generated by Django 2.2.1 on 2019-07-17 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_post_users_downvoted'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='area',
            field=models.CharField(default='Bengaluru', max_length=40),
        ),
        migrations.AddField(
            model_name='post',
            name='domain',
            field=models.CharField(default='others', max_length=40),
        ),
    ]
