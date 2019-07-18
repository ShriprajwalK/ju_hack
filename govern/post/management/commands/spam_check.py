from django.core.management.base import BaseCommand
from post.models import Post

class Command(BaseCommand):
    help = 'check entries for spam.'

    def handle(self, *args, **kwargs):
        posts = Post.objects.all()
        with open("check.txt", 'w') as f:
            for post in posts:
                f.write(("[{" + str(post.content) + "}]" + ","))
        with open('int01.txt', 'r') as f:
            values = f.read()
            is_spam = [int(i) for i in values.split(',')[:-1]]
            ct = 0
            for post in posts:
                post.is_spam = is_spam[ct]
                post.save()
                print(post.is_spam)
                ct += 1
