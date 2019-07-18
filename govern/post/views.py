from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
# from .spam import end


def home(request):
    # return HttpResponse("<h1> Site home </h1>")
    context = {
        "posts": Post.objects.all(),
        "title": "POSTS"}
    return render(request, 'post/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'post/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'area', 'domain', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        # if end(form.instance.content)==1:
        return super().form_valid(form)
        #else:
        #    return redirect(request, 'post-create')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'area', 'domain', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    # return HttpResponse("<h1> ABOUT </h1>")
    return render(request, 'post/about.html')


def upvote(request, *args, **kwargs):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user.username not in str(post.users_upvoted):
            if post.users_upvoted == "":
                post.users_upvoted += str(request.user.username)
            else:
                post.users_upvoted += " " + str(request.user.username)

            post.upvotes = len(post.users_upvoted.split())
            post.save()
        else:
            l = ""
            t = post.users_upvoted.split()
            t.remove(request.user.username)
            for i in t:
                l += i
            post.users_upvoted = l
            post.upvotes = len(post.users_upvoted.split())
            post.save()


        return redirect("post-home")

    else:
        return redirect("login")


def downvote(request, *args, **kwargs):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=kwargs['pk'])
        if request.user.username not in str(post.users_downvoted.split()):
            if post.users_downvoted == "":
                post.users_downvoted += str(request.user.username)
            else:
                post.users_downvoted += " " + str(request.user.username)

            post.downvotes = len(post.users_downvoted.split())
            post.save()
        else:
            l = ""
            t = post.users_downvoted.split()
            t.remove(request.user.username)
            for i in t:
                l += i
            post.users_downvoted = l
            post.downvotes = len(post.users_downvoted.split())
            post.save()


        return redirect("post-home")

    else:
      return redirect("login")
