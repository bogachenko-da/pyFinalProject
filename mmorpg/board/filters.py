from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter, ChoiceFilter
from .models import Post, User
from django import forms


class PostFilter(FilterSet):
    title = CharFilter(
        lookup_expr='icontains',
        label='Название',
    )
    author = ModelChoiceFilter(
        field_name='user',
        queryset=User.objects.all(),
        label='Пользователь',
        empty_label='Все пользователи',
    )
    date = DateFilter(
        field_name='created_at',
        lookup_expr='date__gte',
        label='Позже указанной даты',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    category = ChoiceFilter(
        field_name='category',
        choices=Post.CATEGORY,
        label='Категория',
        empty_label='Все категории',
    )

    class Meta:
        model = Post
        fields = ['title', 'date', 'category']
