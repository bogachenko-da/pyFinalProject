from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .filters import PostFilter
from .forms import PostForm, ReactionForm
from .models import Post, Reaction


class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts_list.html'
    context_object_name = 'posts_list'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['reactions'] = Reaction.objects.filter(accepted=True, post=post)
        return context


class PostsSearchList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts_search.html'
    context_object_name = 'posts_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


class ReactionCreate(LoginRequiredMixin, CreateView):
    form_class = ReactionForm
    model = Reaction
    template_name = 'reaction_create.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)
        form.instance.post = post
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', args=[str(self.kwargs['pk'])])


class ReactionDelete(LoginRequiredMixin, DeleteView):
    model = Reaction
    template_name = 'reaction_delete.html'
    success_url = reverse_lazy('user_reactions')


@login_required
def user_posts(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user).order_by('-created_at')
    return render(request, 'user_posts.html', {'posts': posts})


@login_required
def user_reactions(request):
    current_user = request.user
    reactions = Reaction.objects.filter(user=current_user).order_by('-created_at')
    return render(request, 'user_reactions.html', {'reactions': reactions})


@login_required
def user_posts_reactions(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user).order_by('-created_at')
    selected_post_id = request.GET.get('post')

    reactions = Reaction.objects.filter(post__user=current_user).order_by('-created_at')
    if selected_post_id:
        reactions = reactions.filter(post__id=selected_post_id)

    if request.method == 'GET':
        selected_post_id = request.GET.get('post')
        if selected_post_id:
            reactions = reactions.filter(post__id=selected_post_id)

    return render(request, 'user_posts_reactions.html', {'posts': posts,
                                                         'reactions': reactions,
                                                         'selected_post_id': selected_post_id})


@login_required
def reaction_accept(request, pk):
    reply = get_object_or_404(Reaction, pk=pk)
    reply.accepted = True
    reply.save()
    return HttpResponseRedirect(reverse('user_reactions'))


@login_required
def reaction_reject(request, pk):
    reply = get_object_or_404(Reaction, pk=pk)
    reply.accepted = False
    reply.save()
    return HttpResponseRedirect(reverse('user_reactions'))
