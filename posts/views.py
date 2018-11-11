from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, reverse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy


from .forms import PostForm, CommentForm
from .models import Post


class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:sign-in')
    template_name = 'posts/new_post.html'
    form_class = PostForm
    queryset = Post.objects.all()
    success_url = '/'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        return super(PostCreateView, self).form_valid(form)


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    login_url = reverse_lazy('accounts:sign-in')
    template_name = 'posts/post_detail.html'
    model = Post
    form_class = CommentForm

    def get_queryset(self):
        return Post.objects.all()

    def get_success_url(self):
        return reverse('posts:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.post_id = self.object.id
        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:sign-in')
    template_name = 'posts/posts_list.html'
    context_object_name = "posts_list"
    paginate_by = 20

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', '')
        order = self.request.GET.get('order_by', 'added')
        if filter_value:
            new_context = Post.objects.filter(title__contains=filter_value)
        elif order == 'liked_by' or order == '-liked_by':
            new_context = Post.objects.annotate(
                liked_by_count=Count('liked_by')).order_by(f'{order}_count')
        else:
            new_context = Post.objects.all().order_by(order)
        return new_context


class PostLikeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:sign-in')

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
        post.save()
        return HttpResponseRedirect(
            reverse('posts:detail', kwargs={'pk': post_id})
        )
