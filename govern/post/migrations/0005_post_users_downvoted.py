# Generated by Django 2.2.1 on 2019-07-17 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_post_users_upvoted'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='users_downvoted',
            field=models.TextField(default=''),
        ),
    ]
