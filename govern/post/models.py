"""Models.py file."""
# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    area = models.CharField(max_length=40, default="Bengaluru")
    # domain = models.CharField(max_length=40, default="others")

    DOMAIN_CHOICES = [
    ('IF', 'Infrastructure'),
    ('RD', 'Roads'),
    ('PT', 'Plant Trees'),
    ('AP', 'Animal Problems'),
    ('OTH', 'Others')
    ]
    domain = models.CharField(
        max_length=5,
        choices=DOMAIN_CHOICES,
        default='OTH',
    )

    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_spam = models.IntegerField(default=1)
    is_read = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    users_upvoted = models.TextField(default="")
    users_downvoted = models.TextField(default="")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
